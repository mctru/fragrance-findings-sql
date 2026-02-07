import sqlite3
import csv

conn = sqlite3.connect('fragrances.db')
cursor = conn.cursor()

# Import fragrances
print("Importing fragrances...")
with open('fragrances.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        cursor.execute('''
            INSERT OR REPLACE INTO fragrances 
            (fragrance_id, name, brand, price_usd, bottle_size_ml, category, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (row['fragrance_id'], row['name'], row['brand'], 
              row['price_usd'], row['bottle_size_ml'], row['category'], row['rating']))

# Import notes
print("Importing notes...")
with open('notes.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        cursor.execute('''
            INSERT OR REPLACE INTO notes 
            (note_id, note_name, note_family)
            VALUES (?, ?, ?)
        ''', (row['note_id'], row['note_name'], row['note_family']))

# Import fragrance_notes relationships
print("Importing fragrance-note relationships...")
with open('fragrance_notes.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        cursor.execute('''
            INSERT OR REPLACE INTO fragrance_notes 
            (fragrance_id, note_id, position)
            VALUES (?, ?, ?)
        ''', (row['fragrance_id'], row['note_id'], row['position']))

conn.commit()
conn.close()

print("Data imported successfully!")
