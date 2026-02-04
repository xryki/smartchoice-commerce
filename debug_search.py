from backend.models import DatabaseManager

db = DatabaseManager()

# Test different searches
searches = ['Apple Watch', 'Apple', 'Watch', 'iPhone', 'RTX', 'Samsung']

for search_term in searches:
    products = db.search_products(query=search_term)
    print(f'Search: "{search_term}" -> Found {len(products)} products')
    
    for p in products[:2]:
        print(f'  - {p["name"]} ({p["brand"]}) - {p["price"]}€')
    print()

# Test all products
all_products = db.search_products()
print(f'Total products in database: {len(all_products)}')

for p in all_products:
    print(f'  - {p["name"]} ({p["brand"]}) - {p["price"]}€')
