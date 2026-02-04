from models import DatabaseManager

db = DatabaseManager()

# Test keyword searches
test_searches = [
    'montre',
    'telephone', 
    'tel',
    'portable',
    'ordinateur',
    'pc',
    'carte graphique',
    'gpu',
    'processeur',
    'cpu',
    'ecran',
    'console',
    'souris',
    'apple',
    'samsung',
    'sony',
    'nvidia',
    'amd',
    'logitech',
    'gaming',
    'jeux'
]

print("🔍 Testing Smart Keyword Search")
print("=" * 50)

for search_term in test_searches:
    products = db.search_products(query=search_term)
    print(f"\n🔎 '{search_term}' -> {len(products)} produits trouvés:")
    
    for p in products:
        print(f"  ✅ {p['name']} - {p['price']}€ ({p['brand']})")

print(f"\n🎯 Test completed!")
print("Now test on: http://localhost:5000/products")
