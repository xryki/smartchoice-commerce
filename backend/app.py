from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from recommender import SmartChoiceRecommender
from api_integration import MockProductAPI

app = Flask(__name__, 
           template_folder='../frontend',
           static_folder='../static')
CORS(app)

# Configuration
DATABASE = '../database/products.db'

# Initialize Mock API for real product data
mock_api = MockProductAPI()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database if it doesn't exist"""
    if not os.path.exists(DATABASE):
        # Create database and tables
        conn = get_db()
        cursor = conn.cursor()
        
        # Create products table
        cursor.execute('''
            CREATE TABLE products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                brand TEXT NOT NULL,
                price REAL NOT NULL,
                rating REAL DEFAULT 0,
                quality_score INTEGER DEFAULT 0,
                site TEXT NOT NULL,
                site_reliability INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/debug')
def debug():
    """Debug page for testing API"""
    return render_template('debug.html')

@app.route('/results')
def results():
    """Serve the results page"""
    return render_template('results.html')

@app.route('/api/search', methods=['POST'])
def search_products():
    """Search for products and get recommendations"""
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['budget', 'social_class', 'product', 'category']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        budget = float(data['budget'])
        social_class = data['social_class']
        product_query = data['product'].lower()
        category = data['category']
        
        # Get products from Mock API (real product data with links)
        products = mock_api.search(product_query, category, budget * 1.2)
        
        # If no results from API, fallback to database
        if not products:
            conn = get_db()
            cursor = conn.cursor()
            
            # Search products by name and category
            cursor.execute('''
                SELECT * FROM products 
                WHERE category = ? 
                AND (LOWER(name) LIKE ? OR LOWER(brand) LIKE ?)
                AND price <= ?
                ORDER BY price ASC
            ''', (category, f'%{product_query}%', f'%{product_query}%', budget * 1.2))
            
            products = [dict(row) for row in cursor.fetchall()]
            conn.close()
        
        if not products:
            return jsonify({
                'products': [],
                'recommendations': {},
                'message': 'Aucun produit trouvé pour vos critères'
            })
        
        # Get recommendations
        recommender = SmartChoiceRecommender()
        recommendations = recommender.get_recommendations(products, budget, social_class)
        
        return jsonify({
            'products': products,
            'recommendations': recommendations,
            'total_results': len(products)
        })
        
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({'error': 'Une erreur est survenue lors de la recherche'}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products or filter by category"""
    try:
        category = request.args.get('category')
        conn = get_db()
        cursor = conn.cursor()
        
        if category:
            cursor.execute('SELECT * FROM products WHERE category = ? ORDER BY name', (category,))
        else:
            cursor.execute('SELECT * FROM products ORDER BY category, name')
        
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'products': products})
        
    except Exception as e:
        print(f"Get products error: {e}")
        return jsonify({'error': 'Erreur lors de la récupération des produits'}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all available categories"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT DISTINCT category FROM products ORDER BY category')
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'categories': categories})
        
    except Exception as e:
        print(f"Get categories error: {e}")
        return jsonify({'error': 'Erreur lors de la récupération des catégories'}), 500

@app.route('/api/brands', methods=['GET'])
def get_brands():
    """Get all available brands"""
    try:
        category = request.args.get('category')
        conn = get_db()
        cursor = conn.cursor()
        
        if category:
            cursor.execute('SELECT DISTINCT brand FROM products WHERE category = ? ORDER BY brand', (category,))
        else:
            cursor.execute('SELECT DISTINCT brand FROM products ORDER BY brand')
        
        brands = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'brands': brands})
        
    except Exception as e:
        print(f"Get brands error: {e}")
        return jsonify({'error': 'Erreur lors de la récupération des marques'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Page non trouvée'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Erreur interne du serveur'}), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
