from models_clean import DatabaseManager

db = DatabaseManager()
products = db.search_products()
print(f'Total products: {len(products)}')

for p in products[:5]:
    print(f'- {p["name"]} - {p["price"]}€ ({p["brand"]})')

print('\n🎯 All brands:')
brands = set(p['brand'] for p in products)
for brand in sorted(brands):
    print(f'✅ {brand}')
