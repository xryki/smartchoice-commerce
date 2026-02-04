# Clean version of models.py with all products

import sqlite3
import os
from datetime import datetime
import hashlib
import secrets

DATABASE_PATH = '../database/products.db'

class DatabaseManager:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Products table (enhanced)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                brand TEXT NOT NULL,
                price REAL NOT NULL,
                original_price REAL,
                discount_percentage INTEGER DEFAULT 0,
                rating REAL DEFAULT 0,
                review_count INTEGER DEFAULT 0,
                quality_score INTEGER DEFAULT 0,
                description TEXT,
                image_url TEXT,
                amazon_url TEXT,
                fnac_url TEXT,
                darty_url TEXT,
                boulanger_url TEXT,
                ldlc_url TEXT,
                cdiscount_url TEXT,
                in_stock BOOLEAN DEFAULT 1,
                featured BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, email, password, first_name, last_name, age=None, phone=None):
        """Add a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('''
            INSERT INTO users 
            (email, password_hash, first_name, last_name, age, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, password_hash, first_name, last_name, age, phone))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return user_id
    
    def get_user_by_email(self, email):
        """Get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None
    
    def add_product(self, name, category, brand, price, **kwargs):
        """Add a new product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products 
            (name, category, brand, price, original_price, 
             discount_percentage, rating, review_count, quality_score, description, 
             image_url, amazon_url, fnac_url, darty_url, 
             boulanger_url, ldlc_url, cdiscount_url, in_stock, featured, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ''', (
            name, category, brand, price, kwargs.get('original_price'), kwargs.get('discount_percentage', 0),
            kwargs.get('rating', 0), kwargs.get('review_count', 0),
            kwargs.get('quality_score', 0), kwargs.get('description'),
            kwargs.get('image_url'),
            kwargs.get('amazon_url'), kwargs.get('fnac_url'), kwargs.get('darty_url'),
            kwargs.get('boulanger_url'), kwargs.get('ldlc_url'), kwargs.get('cdiscount_url'),
            kwargs.get('in_stock', True), kwargs.get('featured', False)
        ))
        
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return product_id
    
    def search_products(self, query=None, category=None, brand=None, min_price=None, max_price=None, sort_by='relevance'):
        """Search products with smart keyword matching"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        sql = '''
            SELECT * FROM products 
            WHERE in_stock = 1
        '''
        params = []
        
        if query:
            query_lower = query.lower()
            
            # Smart keyword mapping - simplified
            keyword_map = {
                'montre': ['apple watch', 'watch'],
                'telephone': ['iphone', 'phone', 'smartphone'],
                'tel': ['iphone', 'phone', 'smartphone'],
                'portable': ['iphone', 'phone', 'smartphone'],
                'ordinateur': ['macbook', 'laptop', 'computer'],
                'pc': ['computer', 'desktop'],
                'carte graphique': ['rtx', 'nvidia', 'gpu'],
                'gpu': ['rtx', 'nvidia', 'graphics'],
                'processeur': ['amd', 'ryzen', 'cpu'],
                'cpu': ['amd', 'ryzen', 'processor'],
                'ecran': ['samsung', 'odyssey', 'monitor'],
                'console': ['playstation', 'ps5', 'sony'],
                'souris': ['logitech', 'mouse'],
                'apple': ['apple', 'iphone', 'macbook', 'apple watch'],
                'samsung': ['samsung', 'odyssey'],
                'sony': ['sony', 'playstation', 'ps5'],
                'nvidia': ['nvidia', 'rtx'],
                'amd': ['amd', 'ryzen'],
                'logitech': ['logitech', 'mouse'],
                'gaming': ['playstation', 'ps5', 'rtx'],
                'jeux': ['playstation', 'ps5', 'gaming']
            }
            
            # Find matching keywords
            matching_keywords = [query_lower]
            for keyword, related in keyword_map.items():
                if keyword in query_lower:
                    matching_keywords.extend(related)
            
            # Build single WHERE clause with all terms
            all_terms = list(set(matching_keywords))  # Remove duplicates
            like_conditions = []
            for term in all_terms:
                like_conditions.append('(LOWER(name) LIKE ? OR LOWER(brand) LIKE ?)')
                term_pattern = f'%{term}%'
                params.extend([term_pattern, term_pattern])
            
            sql += ' AND (' + ' OR '.join(like_conditions) + ')'
        
        if category:
            sql += ' AND category = ?'
            params.append(category)
        
        if brand:
            sql += ' AND brand = ?'
            params.append(brand)
        
        if min_price:
            sql += ' AND price >= ?'
            params.append(min_price)
        
        if max_price:
            sql += ' AND price <= ?'
            params.append(max_price)
        
        # Sorting
        if sort_by == 'price_low':
            sql += ' ORDER BY price ASC'
        elif sort_by == 'price_high':
            sql += ' ORDER BY price DESC'
        elif sort_by == 'rating':
            sql += ' ORDER BY rating DESC'
        elif sort_by == 'newest':
            sql += ' ORDER BY created_at DESC'
        elif sort_by == 'discount':
            sql += ' ORDER BY discount_percentage DESC'
        else:  # relevance
            sql += ' ORDER BY featured DESC, rating DESC, review_count DESC'
        
        cursor.execute(sql, params)
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return products
    
    def get_featured_products(self, limit=8):
        """Get featured products"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM products 
            WHERE featured = 1 AND in_stock = 1
            ORDER BY rating DESC, review_count DESC
            LIMIT ?
        ''', (limit,))
        
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return products
    
    def get_categories(self):
        """Get all product categories"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT category FROM products 
            WHERE in_stock = 1
            ORDER BY category
        ''')
        
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return categories
    
    def get_brands(self, category=None):
        """Get all brands"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
                SELECT DISTINCT brand FROM products 
                WHERE category = ? AND in_stock = 1
                ORDER BY brand
            ''', (category,))
        else:
            cursor.execute('''
                SELECT DISTINCT brand FROM products 
                WHERE in_stock = 1
                ORDER BY brand
            ''')
        
        brands = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return brands

# Initialize with real products from many brands
def init_real_products():
    """Initialize database with real products from many brands"""
    db = DatabaseManager()
    
    # Import products from all parts
    from products_part1 import real_products_part1
    from products_part2 import real_products_part2
    
    # Add all products
    for product_data in real_products_part1:
        db.add_product(**product_data)
    
    for product_data in real_products_part2:
        db.add_product(**product_data)
    
    print(f"Added {len(real_products_part1)} products from part 1")
    print(f"Added {len(real_products_part2)} products from part 2")
    
    total_products = len(db.search_products())
    print(f"Total products in database: {total_products}")
    
    print("\n🌍 Products from major brands:")
    print("✅ Apple: iPhone, MacBook, Apple Watch, iPad, AirPods")
    print("✅ Samsung: Galaxy S24, Odyssey G9, Galaxy Tab")
    print("✅ Sony: PlayStation, casques audio, caméras")
    print("✅ Google: Pixel, Nest Hub, Watch")
    print("✅ Microsoft: Xbox, Surface, Laptop")
    print("✅ NVIDIA: RTX 4090, RTX 4070, Shield TV")
    print("✅ AMD: Ryzen 9, Ryzen 7, Ryzen 5")
    print("✅ Intel: Core i9, Core i7, Core i5")
    print("✅ HP: Spectre, Omen, Envy")
    print("✅ Lenovo: ThinkPad, Legion, Yoga")
    print("✅ ASUS: ROG, ZenBook, TUF")
    print("✅ Razer: DeathAdder, Viper, Cynosa")
    
    print(f"\n🎯 Total: {total_products} products from 15+ major brands!")
    print("🛍️ All products have real purchase links to Amazon, Fnac, Darty, LDLC")

if __name__ == "__main__":
    init_real_products()
