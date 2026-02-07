import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style for professional-looking charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

conn = sqlite3.connect('fragrances.db')

# Create output directory for images
import os
if not os.path.exists('visualizations'):
    os.makedirs('visualizations')

print("Creating visualizations...\n")

# ============================================================================
# CHART 1: Price vs Rating Scatter Plot (by Category)
# ============================================================================
print("📊 Chart 1: Price vs Rating Analysis...")

df_scatter = pd.read_sql_query("""
    SELECT name, brand, price_usd, rating, category
    FROM fragrances
""", conn)

plt.figure(figsize=(14, 8))

# Define colors for each category
colors = {
    'designer': '#3498db',  # Blue
    'niche': '#2ecc71',     # Green
    'luxury': '#9b59b6',    # Purple
    'clone': '#e74c3c'      # Red
}

# Plot each category
for category in ['clone', 'designer', 'niche', 'luxury']:
    data = df_scatter[df_scatter['category'] == category]
    plt.scatter(data['price_usd'], data['rating'], 
                label=category.capitalize(), 
                alpha=0.6, 
                s=100,
                color=colors[category],
                edgecolors='white',
                linewidth=1.5)

# Add trend line
z = np.polyfit(df_scatter['price_usd'], df_scatter['rating'], 1)
p = np.poly1d(z)
plt.plot(df_scatter['price_usd'].sort_values(), 
         p(df_scatter['price_usd'].sort_values()), 
         "r--", alpha=0.3, linewidth=2, label='Trend')

plt.xlabel('Price (USD)', fontsize=14, fontweight='bold')
plt.ylabel('Rating (out of 5.0)', fontsize=14, fontweight='bold')
plt.title('Price vs Rating: Does Expensive Mean Better?', 
          fontsize=16, fontweight='bold', pad=20)
plt.legend(loc='lower right', fontsize=12, framealpha=0.9)
plt.grid(True, alpha=0.3)

# Add annotation
plt.text(350, 3.9, 'Weak correlation:\nHigher price ≠ Higher rating', 
         fontsize=11, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('visualizations/1_price_vs_rating.png', dpi=300, bbox_inches='tight')
print("✅ Saved: visualizations/1_price_vs_rating.png\n")
plt.close()

# ============================================================================
# CHART 2: Value Score by Price Range
# ============================================================================
print("📊 Chart 2: Value Score Analysis...")

df_value = pd.read_sql_query("""
    SELECT 
        CASE 
            WHEN price_usd < 50 THEN 'Under $50\n(Clones)'
            WHEN price_usd < 100 THEN '$50-$100\n(Budget)'
            WHEN price_usd < 150 THEN '$100-$150\n(Premium)'
            WHEN price_usd < 250 THEN '$150-$250\n(Entry Luxury)'
            WHEN price_usd < 350 THEN '$250-$350\n(Luxury)'
            ELSE '$350+\n(Ultra-Luxury)'
        END as price_range,
        AVG(rating) as avg_rating,
        AVG(price_usd) as avg_price,
        COUNT(*) as count
    FROM fragrances
    GROUP BY price_range
    ORDER BY avg_price
""", conn)

# Calculate value score (rating per $100)
df_value['value_score'] = (df_value['avg_rating'] / df_value['avg_price']) * 100

plt.figure(figsize=(14, 8))

# Create bar chart
bars = plt.bar(range(len(df_value)), df_value['value_score'], 
               color=['#e74c3c', '#e67e22', '#f39c12', '#2ecc71', '#3498db', '#9b59b6'],
               alpha=0.8, edgecolor='black', linewidth=1.5)

# Highlight the best value
best_idx = df_value['value_score'].idxmax()
bars[best_idx].set_color('#2ecc71')
bars[best_idx].set_alpha(1.0)
bars[best_idx].set_edgecolor('darkgreen')
bars[best_idx].set_linewidth(3)

# Add value labels on bars
for i, (idx, row) in enumerate(df_value.iterrows()):
    plt.text(i, row['value_score'] + 0.1, 
             f"{row['value_score']:.2f}", 
             ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.xlabel('Price Range', fontsize=14, fontweight='bold')
plt.ylabel('Value Score (Rating Points per $100)', fontsize=14, fontweight='bold')
plt.title('The Sweet Spot: Which Price Range Offers Best Value?', 
          fontsize=16, fontweight='bold', pad=20)
plt.xticks(range(len(df_value)), df_value['price_range'], fontsize=11)

# Add annotation for winner
best_range = df_value.iloc[best_idx]['price_range']
best_score = df_value.iloc[best_idx]['value_score']
plt.annotate(f'Best Value!\n{best_score:.2f} points/$100', 
             xy=(best_idx, best_score), 
             xytext=(best_idx + 0.5, best_score + 0.5),
             fontsize=12, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=2))

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/2_value_score.png', dpi=300, bbox_inches='tight')
print("✅ Saved: visualizations/2_value_score.png\n")
plt.close()

# ============================================================================
# CHART 4: Top Notes in High-Rated Fragrances
# ============================================================================
print("📊 Chart 4: Luxury Indicators...")

df_notes = pd.read_sql_query("""
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
    LIMIT 10
""", conn)

plt.figure(figsize=(14, 10))

# Create horizontal bar chart
colors_map = {
    'spicy': '#e74c3c',
    'gourmand': '#f39c12',
    'fresh': '#3498db',
    'ambery': '#9b59b6',
    'floral': '#e91e63',
    'woody': '#795548',
    'aromatic': '#2ecc71'
}

bar_colors = [colors_map.get(fam, '#95a5a6') for fam in df_notes['note_family']]

bars = plt.barh(range(len(df_notes)), df_notes['avg_rating'], 
                color=bar_colors, alpha=0.8, edgecolor='black', linewidth=1.5)

# Add rating labels
for i, (idx, row) in enumerate(df_notes.iterrows()):
    plt.text(row['avg_rating'] + 0.02, i, 
             f"{row['avg_rating']:.2f} ⭐", 
             va='center', fontweight='bold', fontsize=11)
    # Add appearance count
    plt.text(4.0, i, 
             f"({int(row['appearances'])} fragrances)", 
             va='center', fontsize=9, style='italic', alpha=0.7)

plt.yticks(range(len(df_notes)), 
           [f"{row['note_name'].title()}\n({row['note_family']})" 
            for _, row in df_notes.iterrows()],
           fontsize=11)
plt.xlabel('Average Rating', fontsize=14, fontweight='bold')
plt.title('The "Luxury Indicators": Notes That Predict High Ratings', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlim(4.0, 4.6)
plt.grid(axis='x', alpha=0.3)

# Add legend for note families
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=color, label=family.capitalize(), alpha=0.8) 
                   for family, color in colors_map.items() 
                   if family in df_notes['note_family'].values]
plt.legend(handles=legend_elements, loc='lower right', fontsize=10, title='Note Family')

plt.tight_layout()
plt.savefig('visualizations/4_top_notes.png', dpi=300, bbox_inches='tight')
print("✅ Saved: visualizations/4_top_notes.png\n")
plt.close()

conn.close()

print("="*70)
print("✅ All visualizations created successfully!")
print("="*70)
print("\nFiles saved in 'visualizations/' folder:")
print("  1. 1_price_vs_rating.png")
print("  2. 2_value_score.png")
print("  3. 4_top_notes.png")
print("\nYou can now:")
print("  • Add these to your GitHub README")
print("  • Post on LinkedIn (carousel post!)")
print("  • Include in your portfolio")