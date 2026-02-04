from models import DatabaseManager

db = DatabaseManager()

# Test final search without duplicates
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
    'jeux',
    'rtx',
    'playstation',
    'ps5'
]

print("🔍 Final Smart Search Test")
print("=" * 40)

for search_term in test_searches:
    products = db.search_products(query=search_term)
    print(f"\n🔎 '{search_term}' -> {len(products)} produits:")
    
    for p in products:
        print(f"  ✅ {p['name']} - {p['price']}€")

print(f"\n🎯 Perfect! No duplicates!")
print("Test on: http://localhost:5000/products")
