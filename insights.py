import sqlite3
import pandas as pd

conn = sqlite3.connect('fragrances.db')

print("=== OPTIMAL 10-FRAGRANCE COLLECTION ===")
print("(Maximizing note diversity while considering ratings)\n")

# Strategy: Iteratively select fragrances that add the most unique notes
# while maintaining high ratings

# First, get all fragrances with their note counts and ratings
df = pd.read_sql_query("""
    SELECT f.fragrance_id, f.name, f.brand, f.price_usd, f.rating, f.category,
           COUNT(DISTINCT fn.note_id) as unique_notes,
           COUNT(DISTINCT n.note_family) as unique_families,
           GROUP_CONCAT(DISTINCT n.note_family) as families
    FROM fragrances f
    JOIN fragrance_notes fn ON f.fragrance_id = fn.fragrance_id
    JOIN notes n ON fn.note_id = n.note_id
    GROUP BY f.fragrance_id
    ORDER BY unique_notes DESC, rating DESC
""", conn)

print("Top 20 fragrances by note diversity:\n")
print(df.head(20)[['name', 'brand', 'unique_notes', 'unique_families', 'rating', 'price_usd']].to_string(index=False))
print("\n" + "="*80 + "\n")

# Now let's build an optimized collection using a greedy algorithm
print("BUILDING OPTIMIZED 10-FRAGRANCE COLLECTION...")
print("(Algorithm: Greedy selection maximizing new note coverage)\n")

# Get all notes for each fragrance
fragrance_notes = {}
for frag_id in df['fragrance_id']:
    notes_df = pd.read_sql_query(f"""
        SELECT DISTINCT n.note_id, n.note_name, n.note_family
        FROM fragrance_notes fn
        JOIN notes n ON fn.note_id = n.note_id
        WHERE fn.fragrance_id = {frag_id}
    """, conn)
    fragrance_notes[frag_id] = set(notes_df['note_id'])

# Greedy algorithm with rating consideration
selected = []
covered_notes = set()
covered_families = set()

# Pre-filter: only consider fragrances with rating >= 4.0
candidates = df[df['rating'] >= 4.0].copy()

for i in range(10):
    best_score = -1
    best_frag = None
    
    for _, row in candidates.iterrows():
        frag_id = row['fragrance_id']
        if frag_id in [s['fragrance_id'] for s in selected]:
            continue
            
        # Calculate how many NEW notes this fragrance adds
        new_notes = fragrance_notes[frag_id] - covered_notes
        
        # Get family diversity for this fragrance
        frag_families = set(row['families'].split(','))
        new_families = frag_families - covered_families
        
        # Score: prioritize new notes, with bonus for high rating and new families
        score = len(new_notes) * 10 + len(new_families) * 5 + row['rating'] * 2
        
        # Penalty for very high price (diminishing returns)
        if row['price_usd'] > 300:
            score -= 2
            
        if score > best_score:
            best_score = score
            best_frag = row
    
    if best_frag is not None:
        selected.append({
            'fragrance_id': best_frag['fragrance_id'],
            'name': best_frag['name'],
            'brand': best_frag['brand'],
            'price_usd': best_frag['price_usd'],
            'rating': best_frag['rating'],
            'category': best_frag['category'],
            'new_notes': len(fragrance_notes[best_frag['fragrance_id']] - covered_notes),
            'total_notes': len(fragrance_notes[best_frag['fragrance_id']])
        })
        covered_notes.update(fragrance_notes[best_frag['fragrance_id']])
        
        # Update covered families
        frag_families = set(best_frag['families'].split(','))
        covered_families.update(frag_families)

print(f"OPTIMAL 10-FRAGRANCE COLLECTION")
print(f"Total unique notes covered: {len(covered_notes)}")
print(f"Total unique note families covered: {len(covered_families)}\n")

collection_df = pd.DataFrame(selected)
collection_df.index = range(1, 11)
print(collection_df[['name', 'brand', 'category', 'rating', 'price_usd', 'new_notes', 'total_notes']].to_string())

print(f"\n{'='*80}")
print(f"COLLECTION SUMMARY:")
print(f"{'='*80}")
print(f"Total Cost: ${collection_df['price_usd'].sum():.0f}")
print(f"Average Price: ${collection_df['price_usd'].mean():.0f}")
print(f"Average Rating: {collection_df['rating'].mean():.2f}")
print(f"Category Breakdown:")
for cat in collection_df['category'].value_counts().items():
    print(f"  - {cat[0].capitalize()}: {cat[1]}")
print(f"\nNote Families Covered: {', '.join(sorted(covered_families))}")

# Show what note families are in the collection
print(f"\n{'='*80}")
print("DETAILED NOTE FAMILY COVERAGE:")
print(f"{'='*80}\n")

for idx, frag in enumerate(selected, 1):
    frag_id = frag['fragrance_id']
    notes_detail = pd.read_sql_query(f"""
        SELECT DISTINCT n.note_family, COUNT(*) as count
        FROM fragrance_notes fn
        JOIN notes n ON fn.note_id = n.note_id
        WHERE fn.fragrance_id = {frag_id}
        GROUP BY n.note_family
        ORDER BY count DESC
    """, conn)
    print(f"{idx}. {frag['name']} ({frag['brand']})")
    families_str = ", ".join([f"{row['note_family']}({row['count']})" for _, row in notes_detail.iterrows()])
    print(f"   {families_str}\n")

conn.close()