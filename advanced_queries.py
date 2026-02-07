import sqlite3
import pandas as pd

conn = sqlite3.connect('fragrances.db')

# Query 1: Top note combinations in highest-rated fragrances (4.5+)
print("=== Most Common Note Combinations in Top-Rated Fragrances (4.5+) ===")
df = pd.read_sql_query("""
    SELECT n1.note_name as note1, n2.note_name as note2, COUNT(*) as frequency
    FROM fragrances f
    JOIN fragrance_notes fn1 ON f.fragrance_id = fn1.fragrance_id
    JOIN fragrance_notes fn2 ON f.fragrance_id = fn2.fragrance_id
    JOIN notes n1 ON fn1.note_id = n1.note_id
    JOIN notes n2 ON fn2.note_id = n2.note_id
    WHERE f.rating >= 4.5 
    AND n1.note_id < n2.note_id
    GROUP BY n1.note_name, n2.note_name
    ORDER BY frequency DESC
    LIMIT 15
""", conn)
print(df)
print("\n")

# Query 2: Average rating by note family
print("=== Average Rating by Note Family ===")
df = pd.read_sql_query("""
    SELECT n.note_family, 
           AVG(f.rating) as avg_rating,
           COUNT(DISTINCT f.fragrance_id) as fragrance_count
    FROM fragrances f
    JOIN fragrance_notes fn ON f.fragrance_id = fn.fragrance_id
    JOIN notes n ON fn.note_id = n.note_id
    GROUP BY n.note_family
    HAVING fragrance_count >= 5
    ORDER BY avg_rating DESC
""", conn)
print(df)
print("\n")

# Query 3: Designer vs Niche vs Luxury - note profile differences
print("=== Note Family Distribution by Category ===")
df = pd.read_sql_query("""
    SELECT f.category, n.note_family, COUNT(*) as count
    FROM fragrances f
    JOIN fragrance_notes fn ON f.fragrance_id = fn.fragrance_id
    JOIN notes n ON fn.note_id = n.note_id
    WHERE f.category IN ('designer', 'niche', 'luxury')
    GROUP BY f.category, n.note_family
    ORDER BY f.category, count DESC
""", conn)
print(df.head(30))
print("\n")

# Query 4: Most versatile notes (appear across all price ranges)
print("=== Most Versatile Notes (Across All Price Ranges) ===")
df = pd.read_sql_query("""
    SELECT n.note_name, 
           COUNT(DISTINCT CASE WHEN f.price_usd < 100 THEN f.fragrance_id END) as under_100,
           COUNT(DISTINCT CASE WHEN f.price_usd BETWEEN 100 AND 200 THEN f.fragrance_id END) as range_100_200,
           COUNT(DISTINCT CASE WHEN f.price_usd > 200 THEN f.fragrance_id END) as over_200,
           COUNT(DISTINCT f.fragrance_id) as total
    FROM notes n
    JOIN fragrance_notes fn ON n.note_id = fn.note_id
    JOIN fragrances f ON fn.fragrance_id = f.fragrance_id
    GROUP BY n.note_name
    HAVING under_100 > 0 AND range_100_200 > 0 AND over_200 > 0
    ORDER BY total DESC
    LIMIT 15
""", conn)
print(df)
print("\n")

# Query 5: Highest-rated fragrances by category
print("=== Top 5 Fragrances by Category ===")
for category in ['designer', 'niche', 'luxury', 'clone']:
    print(f"\n{category.upper()}:")
    df = pd.read_sql_query(f"""
        SELECT name, brand, price_usd, rating
        FROM fragrances
        WHERE category = '{category}'
        ORDER BY rating DESC, price_usd DESC
        LIMIT 5
    """, conn)
    print(df.to_string(index=False))

print("\n")

# Query 6: Price vs Rating correlation by brand
print("=== Average Rating and Price by Brand (min 3 fragrances) ===")
df = pd.read_sql_query("""
    SELECT brand, 
           COUNT(*) as fragrance_count,
           AVG(price_usd) as avg_price,
           AVG(rating) as avg_rating
    FROM fragrances
    GROUP BY brand
    HAVING fragrance_count >= 3
    ORDER BY avg_rating DESC
""", conn)
print(df)
print("\n")

conn.close()