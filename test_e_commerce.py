import requests

# Test the e-commerce API
base_url = "http://localhost:5000"

def test_products_api():
    """Test the products API"""
    print("=== Testing Products API ===")
    
    # Test featured products
    try:
        response = requests.get(f"{base_url}/api/products/featured")
        print(f"Featured products status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data['products'])} featured products")
            
            for i, product in data['products'][:3]:
                print(f"  {i+1}. {product['name']} - {product['price']}€")
                print(f"     Available at: Amazon, Fnac, Darty")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error connecting to API: {e}")

def test_search_api():
    """Test the search API"""
    print("\n=== Testing Search API ===")
    
    search_data = {
        "query": "Apple Watch",
        "category": "electronics",
        "sort_by": "price_low"
    }
    
    try:
        response = requests.post(f"{base_url}/api/search", json=search_data)
        print(f"Search status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['total']} products for 'Apple Watch'")
            
            for i, product in data['products'][:3]:
                print(f"  {i+1}. {product['name']}")
                print(f"     Price: {product['price']}€")
                print(f"     Rating: {product['rating']}/5")
                print(f"     Available at: Amazon, Fnac, Darty")
                print(f"     Links: Amazon: {product.get('amazon_url', 'N/A')}")
                print(f"     Fnac: {product.get('fnac_url', 'N/A')}")
                print(f"     Darty: {product.get('darty_url', 'N/A')}")
                print()
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error connecting to API: {e}")

def test_auth_api():
    """Test the authentication API"""
    print("\n=== Testing Authentication API ===")
    
    # Test registration
    register_data = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "age": 25
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/register", json=register_data)
        print(f"Registration status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Registration successful!")
            print(f"User ID: {data['user']['id']}")
            print(f"Email: {data['user']['email']}")
            print(f"Token: {data['token'][:50]}...")
            return data['token']
        else:
            print(f"Registration failed: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    return None

if __name__ == "__main__":
    print("🧪 Testing SmartChoice E-Commerce API")
    print("=" * 50)
    
    # Test products
    test_products_api()
    
    # Test search
    test_search_api()
    
    print("\n🎯 Test completed!")
    print("Open http://localhost:5000/products in your browser")
