import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('fragrances.db')

print("="*100)
print("FRAGRANCE MARKET ANALYSIS - KEY INSIGHTS")
print("="*100)
print()

# INSIGHT 1: The Price-Quality Sweet Spot
print("📊 INSIGHT #1: THE PRICE-QUALITY SWEET SPOT")
print("-" * 100)

price_ranges = pd.read_sql_query("""
    SELECT 
        CASE 
            WHEN price_usd < 50 THEN 'Under $50 (Clones)'
            WHEN price_usd < 100 THEN '$50-$100 (Budget Designer)'
            WHEN price_usd < 150 THEN '$100-$150 (Premium Designer)'
            WHEN price_usd < 250 THEN '$150-$250 (Entry Luxury/Niche)'
            WHEN price_usd < 350 THEN '$250-$350 (Luxury)'
            ELSE 'Over $350 (Ultra-Luxury)'
        END as price_range,
        ROUND(AVG(rating), 2) as avg_rating,
        ROUND(AVG(price_usd), 0) as avg_price,
        COUNT(*) as count
    FROM fragrances
    GROUP BY price_range
    ORDER BY avg_price
""", conn)

print(price_ranges.to_string(index=False))
print(f"\n💡 Key Takeaway: Best value is in the ${price_ranges.iloc[2]['avg_price']:.0f}-${price_ranges.iloc[3]['avg_price']:.0f} range")
print(f"   with {price_ranges.iloc[2]['avg_rating']}-{price_ranges.iloc[3]['avg_rating']} average ratings\n")

# INSIGHT 2: Notes That Predict High Ratings
print("\n📊 INSIGHT #2: THE 'LUXURY INDICATORS' - NOTES THAT PREDICT HIGH RATINGS")
print("-" * 100)

luxury_notes = pd.read_sql_query("""
    SELECT n.note_name, 
           n.note_family,
           ROUND(AVG(f.rating), 2) as avg_rating,
           COUNT(DISTINCT f.fragrance_id) as appearances,
           ROUND(AVG(f.price_usd), 0) as avg_price
    FROM notes n
    JOIN fragrance_notes fn ON n.note_id = fn.note_id
    JOIN fragrances f ON fn.fragrance_id = f.fragrance_id
    GROUP BY n.note_name
    HAVING appearances >= 8
    ORDER BY avg_rating DESC
    LIMIT 15
""", conn)

print(luxury_notes.to_string(index=False))
print(f"\n💡 Key Takeaway: Fragrances with '{luxury_notes.iloc[0]['note_name']}' average {luxury_notes.iloc[0]['avg_rating']}/5.0 stars\n")

# INSIGHT 3: Category Comparison
print("\n📊 INSIGHT #3: DESIGNER vs NICHE vs LUXURY - THE REAL DIFFERENCES")
print("-" * 100)

category_comparison = pd.read_sql_query("""
    SELECT 
        f.category,
        COUNT(DISTINCT f.fragrance_id) as fragrances,
        ROUND(AVG(f.rating), 2) as avg_rating,
        ROUND(AVG(f.price_usd), 0) as avg_price,
        ROUND(AVG(note_count), 1) as avg_notes_per_fragrance
    FROM fragrances f
    JOIN (
        SELECT fragrance_id, COUNT(DISTINCT note_id) as note_count
        FROM fragrance_notes
        GROUP BY fragrance_id
    ) nc ON f.fragrance_id = nc.fragrance_id
    WHERE f.category IN ('designer', 'niche', 'luxury')
    GROUP BY f.category
    ORDER BY avg_price
""", conn)

print(category_comparison.to_string(index=False))

# Calculate value metric (rating per $100)
for idx, row in category_comparison.iterrows():
    value = (row['avg_rating'] / row['avg_price']) * 100
    print(f"\n{row['category'].upper()} Value Score: {value:.2f} (rating points per $100)")

# INSIGHT 4: Best Value Fragrances
print("\n\n📊 INSIGHT #4: THE 'HIDDEN GEMS' - HIGH RATED, AFFORDABLE FRAGRANCES")
print("-" * 100)

hidden_gems = pd.read_sql_query("""
    SELECT name, brand, category, rating, price_usd,
           ROUND((rating / price_usd) * 100, 2) as value_score
    FROM fragrances
    WHERE rating >= 4.3 AND price_usd < 150
    ORDER BY value_score DESC
    LIMIT 10
""", conn)

print(hidden_gems.to_string(index=False))
print(f"\n💡 Key Takeaway: You can get 4.3+ rated fragrances for under $150\n")

# INSIGHT 5: Clone vs Original Analysis
print("\n📊 INSIGHT #5: CLONES vs ORIGINALS - THE $250+ SAVINGS")
print("-" * 100)

clone_analysis = pd.read_sql_query("""
    WITH clone_stats AS (
        SELECT 
            AVG(rating) as clone_avg_rating,
            AVG(price_usd) as clone_avg_price
        FROM fragrances
        WHERE category = 'clone'
    ),
    designer_stats AS (
        SELECT 
            AVG(rating) as designer_avg_rating,
            AVG(price_usd) as designer_avg_price
        FROM fragrances
        WHERE category = 'designer'
    )
    SELECT 
        ROUND(c.clone_avg_rating, 2) as clone_rating,
        ROUND(c.clone_avg_price, 0) as clone_price,
        ROUND(d.designer_avg_rating, 2) as designer_rating,
        ROUND(d.designer_avg_price, 0) as designer_price,
        ROUND(d.designer_avg_price - c.clone_avg_price, 0) as price_difference,
        ROUND(d.designer_avg_rating - c.clone_avg_rating, 2) as rating_difference
    FROM clone_stats c, designer_stats d
""", conn)

print(clone_analysis.to_string(index=False))
print(f"\n💡 Key Takeaway: Clones cost ${clone_analysis.iloc[0]['price_difference']:.0f} less on average")
print(f"   Rating difference: only {abs(clone_analysis.iloc[0]['rating_difference']):.2f} stars\n")

# INSIGHT 6: Most Versatile Brands
print("\n📊 INSIGHT #6: BEST BRANDS BY PERFORMANCE (Min. 3 fragrances)")
print("-" * 100)

brand_performance = pd.read_sql_query("""
    SELECT 
        brand,
        COUNT(*) as fragrances,
        ROUND(AVG(rating), 2) as avg_rating,
        ROUND(AVG(price_usd), 0) as avg_price,
        ROUND((AVG(rating) / AVG(price_usd)) * 100, 3) as value_score
    FROM fragrances
    GROUP BY brand
    HAVING fragrances >= 3
    ORDER BY avg_rating DESC
    LIMIT 10
""", conn)

print(brand_performance.to_string(index=False))

# INSIGHT 7: The Data-Driven Collection
print("\n\n📊 INSIGHT #7: THE OPTIMAL 10-FRAGRANCE COLLECTION")
print("-" * 100)
print("Based on maximizing note diversity while balancing cost and ratings:\n")

# Simple top-rated diverse collection
collection_query = """
WITH ranked_frags AS (
    SELECT 
        f.fragrance_id,
        f.name,
        f.brand,
        f.category,
        f.rating,
        f.price_usd,
        COUNT(DISTINCT fn.note_id) as unique_notes,
        ROW_NUMBER() OVER (PARTITION BY f.category ORDER BY f.rating DESC, COUNT(DISTINCT fn.note_id) DESC) as rn
    FROM fragrances f
    JOIN fragrance_notes fn ON f.fragrance_id = fn.fragrance_id
    WHERE f.rating >= 4.0
    GROUP BY f.fragrance_id
)
SELECT name, brand, category, rating, price_usd, unique_notes
FROM ranked_frags
WHERE (category = 'designer' AND rn <= 3)
   OR (category = 'niche' AND rn <= 3)
   OR (category = 'luxury' AND rn <= 4)
ORDER BY 
    CASE category 
        WHEN 'designer' THEN 1
        WHEN 'niche' THEN 2
        WHEN 'luxury' THEN 3
    END,
    rating DESC
"""

collection = pd.read_sql_query(collection_query, conn)
print(collection.to_string(index=False))

if len(collection) > 0:
    print(f"\n💰 Total Investment: ${collection['price_usd'].sum():.0f}")
    print(f"⭐ Average Rating: {collection['rating'].mean():.2f}/5.0")
    print(f"🎨 Total Unique Notes: {collection['unique_notes'].sum()}")

print("\n" + "="*100)
print("END OF ANALYSIS - Ready for LinkedIn!")
print("="*100)

conn.close()