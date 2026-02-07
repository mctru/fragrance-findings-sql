import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Set up the figure style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']

# ============================================================================
# SLIDE 1: Title Slide
# ============================================================================

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Background gradient effect
gradient = ax.imshow([[0, 0], [1, 1]], extent=[0, 10, 0, 10], 
                     aspect='auto', cmap='Blues', alpha=0.15)

# Main title
ax.text(5, 7.5, 'Fragrance Market Analysis', 
        fontsize=42, weight='bold', ha='center', va='center')

# Subtitle
ax.text(5, 6.5, 'A Data-Driven Investigation', 
        fontsize=24, ha='center', va='center', style='italic', alpha=0.8)

# Key question
ax.text(5, 5, 'Are Expensive Fragrances\nActually Worth It?', 
        fontsize=32, weight='bold', ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='lightblue', 
                 edgecolor='navy', linewidth=3, alpha=0.3))

# Stats box
stats_text = '132 Fragrances Analyzed\n195 Unique Scent Notes\n4 Categories Compared'
ax.text(5, 2.8, stats_text, 
        fontsize=18, ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='white', 
                 edgecolor='gray', linewidth=2))

# Tech stack
ax.text(5, 1.5, 'SQL • Python • Pandas • Data Analysis', 
        fontsize=16, ha='center', va='center', weight='bold', alpha=0.7)

# Author
ax.text(5, 0.5, 'By: Maumin Touqeer | GitHub: github.com/mctru/fragrance-findings-sql', 
        fontsize=12, ha='center', va='center', alpha=0.6)

plt.tight_layout()
plt.savefig('visualizations/0_title_slide.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("✅ Created: visualizations/0_title_slide.png")
plt.close()

# ============================================================================
# SLIDE 5: Key Takeaways
# ============================================================================

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Background
gradient = ax.imshow([[0, 0], [1, 1]], extent=[0, 10, 0, 10], 
                     aspect='auto', cmap='Greens', alpha=0.15)

# Title
ax.text(5, 9, 'Key Takeaways', 
        fontsize=40, weight='bold', ha='center', va='top')

# Takeaway boxes
takeaways = [
    {
        'title': '💰 Clone vs Original',
        'text': 'Save $77 per bottle\nOnly 0.19 star difference',
        'y': 7.5
    },
    {
        'title': '🎯 The Sweet Spot',
        'text': '$100-$150 range offers\n3.9x better value than luxury',
        'y': 5.8
    },
    {
        'title': '🔬 Luxury Indicators',
        'text': 'Tobacco, Saffron, Vanilla\npredict 4.4+ star ratings',
        'y': 4.1
    },
    {
        'title': '📊 The Truth',
        'text': 'Price ≠ Quality\nYou\'re paying for the brand',
        'y': 2.4
    }
]

for item in takeaways:
    # Title
    ax.text(5, item['y'], item['title'], 
            fontsize=24, weight='bold', ha='center', va='top')
    
    # Content
    ax.text(5, item['y'] - 0.4, item['text'], 
            fontsize=18, ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', 
                     edgecolor='orange', linewidth=2, alpha=0.6))

# Call to action
ax.text(5, 0.8, 'Full Analysis & SQL Code', 
        fontsize=22, weight='bold', ha='center', va='center')

ax.text(5, 0.3, 'github.com/mctru/fragrance-findings-sql', 
        fontsize=18, ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='lightblue', 
                 edgecolor='blue', linewidth=2))

plt.tight_layout()
plt.savefig('visualizations/5_takeaways.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("✅ Created: visualizations/5_takeaways.png")
plt.close()

print("\n" + "="*70)
print("✅ Text slides created successfully!")
print("="*70)
print("\nYour complete LinkedIn carousel (in order):")
print("  1. 0_title_slide.png")
print("  2. 1_price_vs_rating.png")
print("  3. 2_value_score.png")
print("  4. 4_top_notes.png")
print("  5. 5_takeaways.png")
print("\nUpload these in this order to LinkedIn!")