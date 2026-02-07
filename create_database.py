import sqlite3

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect('fragrances.db')
cursor = conn.cursor()

# Create Fragrances table
cursor.execute('''
CREATE TABLE IF NOT EXISTS fragrances (
    fragrance_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    price_usd REAL,
    bottle_size_ml INTEGER,
    category TEXT,
    rating REAL
)
''')

# Create Notes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS notes (
    note_id INTEGER PRIMARY KEY,
    note_name TEXT NOT NULL,
    note_family TEXT
)
''')

# Create Fragrance_Notes junction table
cursor.execute('''
CREATE TABLE IF NOT EXISTS fragrance_notes (
    fragrance_id INTEGER,
    note_id INTEGER,
    position TEXT,
    FOREIGN KEY (fragrance_id) REFERENCES fragrances(fragrance_id),
    FOREIGN KEY (note_id) REFERENCES notes(note_id),
    PRIMARY KEY (fragrance_id, note_id, position)
)
''')

conn.commit()
conn.close()

print("Database created successfully!")