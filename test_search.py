import requests

# Test the API directly
url = "http://localhost:5000/api/search"
data = {
    "budget": 1000,
    "social_class": "medium", 
    "product": "Apple",
    "category": "electronics"
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        products = result.get('products', [])
        print(f"\nFound {len(products)} products:")
        for i, product in enumerate(products[:3]):
            print(f"{i+1}. {product.get('name')} - {product.get('price')}€ - {product.get('site')}")
            if product.get('purchase_url'):
                print(f"   Link: {product['purchase_url']}")
    
except Exception as e:
    print(f"Error: {e}")
