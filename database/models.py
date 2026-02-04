"""
Database models for SmartChoice application
"""

import sqlite3
import os
from datetime import datetime

DATABASE_PATH = 'products.db'

class DatabaseManager:
    """Manages database operations for SmartChoice"""
    
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                brand TEXT NOT NULL,
                price REAL NOT NULL,
                rating REAL DEFAULT 0,
                quality_score INTEGER DEFAULT 0,
                site TEXT NOT NULL,
                site_reliability INTEGER DEFAULT 0,
                description TEXT,
                image_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create users table (optional for future features)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                budget REAL,
                social_class TEXT,
                preferences TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create search_history table (optional for analytics)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                search_query TEXT,
                budget REAL,
                social_class TEXT,
                category TEXT,
                results_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def add_product(self, name, category, brand, price, rating=0, 
                   quality_score=0, site='', site_reliability=0, 
                   description='', image_url=''):
        """Add a new product to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products 
            (name, category, brand, price, rating, quality_score, 
             site, site_reliability, description, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, brand, price, rating, quality_score,
              site, site_reliability, description, image_url))
        
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return product_id
    
    def get_products(self, category=None, brand=None, max_price=None, 
                    min_quality=None, min_reliability=None):
        """Get products with optional filters"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if brand:
            query += " AND brand = ?"
            params.append(brand)
        
        if max_price:
            query += " AND price <= ?"
            params.append(max_price)
        
        if min_quality:
            query += " AND quality_score >= ?"
            params.append(min_quality)
        
        if min_reliability:
            query += " AND site_reliability >= ?"
            params.append(min_reliability)
        
        query += " ORDER BY name"
        
        cursor.execute(query, params)
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return products
    
    def search_products(self, query, category=None, max_price=None):
        """Search products by name or brand"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_query = f"%{query.lower()}%"
        
        sql = '''
            SELECT * FROM products 
            WHERE (LOWER(name) LIKE ? OR LOWER(brand) LIKE ?)
        '''
        params = [search_query, search_query]
        
        if category:
            sql += " AND category = ?"
            params.append(category)
        
        if max_price:
            sql += " AND price <= ?"
            params.append(max_price)
        
        sql += " ORDER BY name"
        
        cursor.execute(sql, params)
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return products
    
    def get_categories(self):
        """Get all unique categories"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return categories
    
    def get_brands(self, category=None):
        """Get all unique brands, optionally filtered by category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if category:
            cursor.execute(
                "SELECT DISTINCT brand FROM products WHERE category = ? ORDER BY brand", 
                (category,)
            )
        else:
            cursor.execute("SELECT DISTINCT brand FROM products ORDER BY brand")
        
        brands = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return brands
    
    def update_product(self, product_id, **kwargs):
        """Update product information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        set_clauses = []
        params = []
        
        for key, value in kwargs.items():
            if key in ['name', 'category', 'brand', 'price', 'rating', 
                      'quality_score', 'site', 'site_reliability', 
                      'description', 'image_url']:
                set_clauses.append(f"{key} = ?")
                params.append(value)
        
        if set_clauses:
            set_clauses.append("updated_at = CURRENT_TIMESTAMP")
            params.append(product_id)
            
            query = f"UPDATE products SET {', '.join(set_clauses)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def delete_product(self, product_id):
        """Delete a product from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()
    
    def get_product_stats(self):
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total products
        cursor.execute("SELECT COUNT(*) FROM products")
        stats['total_products'] = cursor.fetchone()[0]
        
        # Products by category
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM products 
            GROUP BY category 
            ORDER BY count DESC
        ''')
        stats['products_by_category'] = dict(cursor.fetchall())
        
        # Average price
        cursor.execute("SELECT AVG(price) FROM products")
        stats['average_price'] = round(cursor.fetchone()[0] or 0, 2)
        
        # Price range
        cursor.execute("SELECT MIN(price), MAX(price) FROM products")
        min_price, max_price = cursor.fetchone()
        stats['price_range'] = {'min': min_price or 0, 'max': max_price or 0}
        
        # Quality distribution
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN quality_score >= 90 THEN 'Excellent'
                    WHEN quality_score >= 70 THEN 'Good'
                    WHEN quality_score >= 50 THEN 'Average'
                    ELSE 'Poor'
                END as quality_level,
                COUNT(*) as count
            FROM products
            GROUP BY quality_level
        ''')
        stats['quality_distribution'] = dict(cursor.fetchall())
        
        conn.close()
        return stats
    
    def record_search(self, user_id=None, search_query='', budget=0, 
                      social_class='', category='', results_count=0):
        """Record a search for analytics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO search_history 
            (user_id, search_query, budget, social_class, category, results_count)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, search_query, budget, social_class, category, results_count))
        
        conn.commit()
        conn.close()

# Sample data initialization
def init_sample_data():
    """Initialize database with sample products"""
    db = DatabaseManager()
    
    sample_products = [
        # Électronique
        {
            'name': 'iPhone 15 Pro',
            'category': 'electronics',
            'brand': 'Apple',
            'price': 1199,
            'rating': 4.8,
            'quality_score': 95,
            'site': 'Amazon',
            'site_reliability': 90,
            'description': 'Dernier modèle iPhone avec processeur A17 Pro'
        },
        {
            'name': 'Galaxy S24 Ultra',
            'category': 'electronics',
            'brand': 'Samsung',
            'price': 1299,
            'rating': 4.7,
            'quality_score': 92,
            'site': 'Fnac',
            'site_reliability': 95,
            'description': 'Smartphone Android haut de gamme avec S Pen'
        },
        {
            'name': 'Pixel 8 Pro',
            'category': 'electronics',
            'brand': 'Google',
            'price': 999,
            'rating': 4.6,
            'quality_score': 88,
            'site': 'Boulanger',
            'site_reliability': 85,
            'description': 'Smartphone Google avec IA avancée'
        },
        {
            'name': 'MacBook Air M2',
            'category': 'electronics',
            'brand': 'Apple',
            'price': 1299,
            'rating': 4.9,
            'quality_score': 96,
            'site': 'Apple Store',
            'site_reliability': 100,
            'description': 'Ordinateur portable ultra-fin avec puce M2'
        },
        {
            'name': 'ThinkPad X1 Carbon',
            'category': 'electronics',
            'brand': 'Lenovo',
            'price': 1499,
            'rating': 4.5,
            'quality_score': 90,
            'site': 'LDLC',
            'site_reliability': 80,
            'description': 'Ordinateur portable professionnel robuste'
        },
        
        # Vêtements
        {
            'name': 'Jean 501 Original',
            'category': 'clothing',
            'brand': 'Levi\'s',
            'price': 89,
            'rating': 4.4,
            'quality_score': 82,
            'site': 'Galeries Lafayette',
            'site_reliability': 88,
            'description': 'Jean classique indémodable'
        },
        {
            'name': 'Vans Old Skool',
            'category': 'clothing',
            'brand': 'Vans',
            'price': 65,
            'rating': 4.3,
            'quality_score': 75,
            'site': 'Foot Locker',
            'site_reliability': 82,
            'description': 'Baskets skateboard classiques'
        },
        {
            'name': 'Hoodie Essential',
            'category': 'clothing',
            'brand': 'Nike',
            'price': 45,
            'rating': 4.2,
            'quality_score': 78,
            'site': 'Zalando',
            'site_reliability': 85,
            'description': 'Sweat à capuche confortable'
        },
        
        # Maison
        {
            'name': 'Aspirateur Robot Roomba',
            'category': 'home',
            'brand': 'iRobot',
            'price': 299,
            'rating': 4.1,
            'quality_score': 85,
            'site': 'Darty',
            'site_reliability': 90,
            'description': 'Aspirateur robot intelligent'
        },
        {
            'name': 'Machine à café Nespresso',
            'category': 'home',
            'brand': 'Nespresso',
            'price': 149,
            'rating': 4.3,
            'quality_score': 80,
            'site': 'Amazon',
            'site_reliability': 90,
            'description': 'Machine à café à capsules'
        },
        
        # Sports
        {
            'name': 'Yoga Mat Pro',
            'category': 'sports',
            'brand': 'Decathlon',
            'price': 29,
            'rating': 4.0,
            'quality_score': 70,
            'site': 'Decathlon',
            'site_reliability': 92,
            'description': 'Tapis de yoga professionnel'
        },
        {
            'name': 'Running Shoes Ultraboost',
            'category': 'sports',
            'brand': 'Adidas',
            'price': 140,
            'rating': 4.5,
            'quality_score': 85,
            'site': 'Go Sport',
            'site_reliability': 78,
            'description': 'Chaussures de running haute performance'
        }
    ]
    
    # Add sample products to database
    for product_data in sample_products:
        db.add_product(**product_data)
    
    print(f"Added {len(sample_products)} sample products to database")

if __name__ == "__main__":
    # Initialize database with sample data
    init_sample_data()
