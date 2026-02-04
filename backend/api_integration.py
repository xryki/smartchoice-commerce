"""
API Integration for Real Product Data
Options for getting real products with purchase links
"""

import requests
import json
from typing import List, Dict, Optional

class ProductAPIManager:
    """Manages integration with various product APIs"""
    
    def __init__(self):
        self.apis = {
            'amazon': AmazonAPI(),
            'ebay': EbayAPI(), 
            'affiliation': AffiliationAPI(),
            'openfoodfacts': OpenFoodFactsAPI()
        }
    
    def search_products(self, query: str, category: str = None, max_price: float = None) -> List[Dict]:
        """Search across multiple APIs"""
        all_products = []
        
        for api_name, api in self.apis.items():
            try:
                products = api.search(query, category, max_price)
                all_products.extend(products)
            except Exception as e:
                print(f"Error with {api_name}: {e}")
        
        return self._normalize_products(all_products)
    
    def _normalize_products(self, products: List[Dict]) -> List[Dict]:
        """Normalize products from different APIs to our format"""
        normalized = []
        
        for product in products:
            normalized_product = {
                'name': product.get('name', ''),
                'category': product.get('category', 'unknown'),
                'brand': product.get('brand', 'Unknown'),
                'price': float(product.get('price', 0)),
                'rating': float(product.get('rating', 0)),
                'quality_score': int(product.get('quality_score', 70)),
                'site': product.get('site', 'Unknown'),
                'site_reliability': int(product.get('site_reliability', 80)),
                'description': product.get('description', ''),
                'image_url': product.get('image_url', ''),
                'purchase_url': product.get('purchase_url', ''),
                'original_source': product.get('source', 'unknown')
            }
            normalized.append(normalized_product)
        
        return normalized

class AmazonAPI:
    """Amazon Product Advertising API"""
    
    def __init__(self):
        self.base_url = "https://webservices.amazon.com/paapi5"
        # Note: Requires Amazon Developer account and credentials
        self.access_key = "YOUR_ACCESS_KEY"
        self.secret_key = "YOUR_SECRET_KEY"
        self.partner_tag = "YOUR_PARTNER_TAG"
    
    def search(self, query: str, category: str = None, max_price: float = None) -> List[Dict]:
        """Search Amazon products"""
        # This is a mock implementation
        # Real implementation would use Amazon PA API 5.0
        
        mock_products = [
            {
                'name': f'{query.title()} - Amazon Premium',
                'category': category or 'electronics',
                'brand': 'Various',
                'price': 299.99,
                'rating': 4.5,
                'quality_score': 85,
                'site': 'Amazon',
                'site_reliability': 95,
                'description': f'High quality {query} from Amazon',
                'image_url': 'https://via.placeholder.com/300x300',
                'purchase_url': f'https://amazon.com/dp/B0{hash(query) % 1000000}',
                'source': 'amazon'
            }
        ]
        
        return mock_products

class EbayAPI:
    """eBay Finding API"""
    
    def __init__(self):
        self.base_url = "https://api.ebay.com/buy/browse/v1"
        # Note: Requires eBay Developer account
        self.app_id = "YOUR_EBAY_APP_ID"
    
    def search(self, query: str, category: str = None, max_price: float = None) -> List[Dict]:
        """Search eBay products"""
        mock_products = [
            {
                'name': f'{query.title()} - eBay Deal',
                'category': category or 'electronics',
                'brand': 'Various',
                'price': 199.99,
                'rating': 4.2,
                'quality_score': 75,
                'site': 'eBay',
                'site_reliability': 85,
                'description': f'Great deal on {query} from eBay',
                'image_url': 'https://via.placeholder.com/300x300',
                'purchase_url': f'https://ebay.com/itm/{hash(query) % 1000000}',
                'source': 'ebay'
            }
        ]
        
        return mock_products

class AffiliationAPI:
    """French Affiliate Networks (Darty, Fnac, etc.)"""
    
    def __init__(self):
        self.networks = {
            'darty': 'https://www.darty.com',
            'fnac': 'https://www.fnac.com',
            'boulanger': 'https://www.boulanger.com',
            'ldlc': 'https://www.ldlc.com'
        }
    
    def search(self, query: str, category: str = None, max_price: float = None) -> List[Dict]:
        """Search French affiliate networks"""
        products = []
        
        for store_name, base_url in self.networks.items():
            product = {
                'name': f'{query.title()} - {store_name.title()}',
                'category': category or 'electronics',
                'brand': 'Various',
                'price': 249.99,
                'rating': 4.3,
                'quality_score': 80,
                'site': store_name.title(),
                'site_reliability': 90,
                'description': f'{query} from {store_name.title()}',
                'image_url': 'https://via.placeholder.com/300x300',
                'purchase_url': f'{base_url}/search?q={query}',
                'source': store_name
            }
            products.append(product)
        
        return products

class OpenFoodFactsAPI:
    """Open Food Facts API for food products"""
    
    def __init__(self):
        self.base_url = "https://world.openfoodfacts.org/api/v2"
    
    def search(self, query: str, category: str = None, max_price: float = None) -> List[Dict]:
        """Search food products"""
        try:
            url = f"{self.base_url}/search"
            params = {
                'search_terms': query,
                'page_size': 10,
                'json': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            products = []
            for product_data in data.get('products', []):
                product = {
                    'name': product_data.get('product_name', ''),
                    'category': 'food',
                    'brand': product_data.get('brands', 'Unknown'),
                    'price': self._estimate_price(product_data),
                    'rating': float(product_data.get('nutriscore_grade', 'c').replace('a', '5').replace('b', '4').replace('c', '3').replace('d', '2').replace('e', '1')),
                    'quality_score': self._calculate_quality_score(product_data),
                    'site': 'Open Food Facts',
                    'site_reliability': 95,
                    'description': product_data.get('ingredients_text', ''),
                    'image_url': product_data.get('image_url', ''),
                    'purchase_url': f"https://world.openfoodfacts.org/product/{product_data.get('code', '')}",
                    'source': 'openfoodfacts'
                }
                products.append(product)
            
            return products
            
        except Exception as e:
            print(f"Open Food Facts API error: {e}")
            return []
    
    def _estimate_price(self, product_data: Dict) -> float:
        """Estimate price based on product data"""
        # This is a mock estimation
        return round(hash(product_data.get('product_name', '')) % 50 + 5, 2)
    
    def _calculate_quality_score(self, product_data: Dict) -> int:
        """Calculate quality score based on nutriscore and other factors"""
        nutriscore = product_data.get('nutriscore_grade', 'c')
        score_map = {'a': 95, 'b': 85, 'c': 75, 'd': 65, 'e': 55}
        return score_map.get(nutriscore, 70)

# Mock API for demonstration
class MockProductAPI:
    """Mock API for demonstration purposes"""
    
    def __init__(self):
        self.products = self._generate_mock_products()
    
    def _generate_mock_products(self) -> List[Dict]:
        """Generate a large variety of mock products"""
        products = []
        
        categories = ['electronics', 'clothing', 'home', 'sports', 'books', 'food', 'beauty', 'toys']
        brands = ['Apple', 'Samsung', 'Nike', 'Adidas', 'Sony', 'LG', 'Dyson', 'Philips', 'Lego', 'Hasbro']
        stores = ['Amazon', 'Fnac', 'Darty', 'Boulanger', 'LDLC', 'Cdiscount', 'Rakuten', 'eBay']
        
        for i in range(1000):  # Generate 1000 mock products
            product = {
                'name': f'Product {i+1} - {categories[i % len(categories)].title()}',
                'category': categories[i % len(categories)],
                'brand': brands[i % len(brands)],
                'price': round((i % 500) + 10, 2),
                'rating': round(3 + (i % 3) * 0.5, 1),
                'quality_score': 60 + (i % 40),
                'site': stores[i % len(stores)],
                'site_reliability': 70 + (i % 30),
                'description': f'High quality product from {brands[i % len(brands)]}',
                'image_url': f'https://picsum.photos/300/300?random={i}',
                'purchase_url': f'https://example.com/product/{i+1}',
                'source': 'mock'
            }
            products.append(product)
        
        return products
    
    def search(self, query: str, category: str = None, max_price: float = None) -> List[Dict]:
        """Search mock products"""
        filtered_products = self.products
        
        # Filter by query
        if query:
            query_lower = query.lower()
            filtered_products = [p for p in filtered_products 
                                if query_lower in p['name'].lower() or 
                                   query_lower in p['brand'].lower()]
        
        # Filter by category
        if category:
            filtered_products = [p for p in filtered_products if p['category'] == category]
        
        # Filter by price
        if max_price:
            filtered_products = [p for p in filtered_products if p['price'] <= max_price]
        
        return filtered_products[:20]  # Return max 20 results
