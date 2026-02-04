# Test final search functionality

import requests
import json

# Test API endpoints
base_url = "http://localhost:5000"

def test_search():
    """Test search functionality"""
    
    # Test keyword searches
    test_queries = [
        "montre",
        "telephone", 
        "ordinateur",
        "carte graphique",
        "processeur",
        "console",
        "apple",
        "samsung",
        "sony",
        "nvidia",
        "amd",
        "gaming"
    ]
    
    print("🔍 Testing Smart Keyword Search")
    print("=" * 50)
    
    for query in test_queries:
        try:
            response = requests.post(
                f"{base_url}/api/search",
                json={"query": query},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                products = data.get('products', [])
                print(f"\n📱 Search: '{query}'")
                print(f"   Found {len(products)} products")
                
                # Show first 3 results
                for i, product in enumerate(products[:3]):
                    print(f"   {i+1}. {product['name']} - {product['price']}€ ({product['brand']})")
                
                if len(products) > 3:
                    print(f"   ... and {len(products) - 3} more")
            else:
                print(f"\n❌ Search '{query}' failed: {response.status_code}")
                
        except Exception as e:
            print(f"\n❌ Error searching '{query}': {e}")
    
    print("\n🎯 Testing Featured Products")
    print("=" * 50)
    
    try:
        response = requests.get(f"{base_url}/api/products/featured")
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"Found {len(products)} featured products")
            
            for i, product in enumerate(products[:5]):
                print(f"{i+1}. {product['name']} - {product['price']}€ ({product['brand']})")
        else:
            print(f"❌ Featured products failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting featured products: {e}")
    
    print("\n🛍️ Testing Categories & Brands")
    print("=" * 50)
    
    try:
        # Categories
        response = requests.get(f"{base_url}/api/categories")
        if response.status_code == 200:
            data = response.json()
            categories = data.get('categories', [])
            print(f"Categories: {', '.join(categories)}")
        
        # Brands
        response = requests.get(f"{base_url}/api/brands")
        if response.status_code == 200:
            data = response.json()
            brands = data.get('brands', [])
            print(f"Brands: {', '.join(brands)}")
            
    except Exception as e:
        print(f"❌ Error getting categories/brands: {e}")

if __name__ == "__main__":
    test_search()
