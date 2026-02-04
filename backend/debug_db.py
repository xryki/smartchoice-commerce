from models import DatabaseManager

db = DatabaseManager()

# Test search
products = db.search_products(query='Apple')
print('Found', len(products), 'products for "Apple"')

for p in products:
    print('- ' + p['name'] + ' - ' + str(p['price']) + '€')

# Check all products
all_products = db.search_products()
print('\nTotal products in database:', len(all_products))

for p in all_products:
    print('- ' + p['name'] + ' (' + p['brand'] + ')')
