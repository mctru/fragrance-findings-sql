import sqlite3
import pandas as pd

conn = sqlite3.connect('fragrances.db')

# Query 1: Show all fragrances with their ratings
print("=== All Fragrances ===")
df = pd.read_sql_query("SELECT * FROM fragrances ORDER BY rating DESC", conn)
print(df)
print("\n")

# Query 2: Average price by category
print("=== Average Price by Category ===")
df = pd.read_sql_query("""
    SELECT category, 
           AVG(price_usd) as avg_price,
           COUNT(*) as count
    FROM fragrances
    GROUP BY category
""", conn)
print(df)
print("\n")

# Query 3: Most common notes across all fragrances
print("=== Most Common Notes ===")
df = pd.read_sql_query("""
    SELECT n.note_name, n.note_family, COUNT(*) as frequency
    FROM fragrance_notes fn
    JOIN notes n ON fn.note_id = n.note_id
    GROUP BY n.note_name
    ORDER BY frequency DESC
    LIMIT 10
""", conn)
print(df)
print("\n")

# Query 4: Most common note families
print("=== Most Common Note Families ===")
df = pd.read_sql_query("""
    SELECT n.note_family, COUNT(*) as frequency
    FROM fragrance_notes fn
    JOIN notes n ON fn.note_id = n.note_id
    GROUP BY n.note_family
    ORDER BY frequency DESC
""", conn)
print(df)
print("\n")

# Query 5: Fragrances with woody notes
print("=== Fragrances with Woody Notes ===")
df = pd.read_sql_query("""
    SELECT DISTINCT f.name, f.brand, f.price_usd, f.rating
    FROM fragrances f
    JOIN fragrance_notes fn ON f.fragrance_id = fn.fragrance_id
    JOIN notes n ON fn.note_id = n.note_id
    WHERE n.note_family = 'woody'
    ORDER BY f.rating DESC
""", conn)
print(df)
print("\n")

# Query 6: Average rating by price range
print("=== Average Rating by Price Range ===")
df = pd.read_sql_query("""
    SELECT 
        CASE 
            WHEN price_usd < 100 THEN 'Under $100'
            WHEN price_usd < 200 THEN '$100-$200'
            ELSE 'Over $200'
        END as price_range,
        AVG(rating) as avg_rating,
        COUNT(*) as count
    FROM fragrances
    GROUP BY price_range
""", conn)
print(df)
print("\n")

conn.close()