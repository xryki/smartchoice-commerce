from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import sqlite3
import os
from models import DatabaseManager
from auth import generate_token, decode_token, token_required
import jwt

app = Flask(__name__, 
           template_folder='../frontend',
           static_folder='../static')
app.secret_key = 'smartchoice_secret_key_2024'
CORS(app)

# Initialize database
db = DatabaseManager()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/login')
def login_page():
    """Serve login page"""
    return render_template('login.html')

@app.route('/register')
def register_page():
    """Serve registration page"""
    return render_template('register.html')

@app.route('/products')
def products_page():
    """Serve products page"""
    return render_template('products.html')

@app.route('/product/<int:product_id>')
def product_detail_page(product_id):
    """Serve product detail page"""
    return render_template('product_detail.html', product_id=product_id)

@app.route('/profile')
@token_required
def profile_page():
    """Serve user profile page"""
    return render_template('profile.html')

# API Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate email format
        if '@' not in data['email']:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Create user
        user_id = db.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data.get('age'),
            phone=data.get('phone')
        )
        
        if user_id:
            # Generate token
            token = generate_token(user_id, data['email'])
            
            return jsonify({
                'message': 'User created successfully',
                'token': token,
                'user': {
                    'id': user_id,
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name']
                }
            }), 201
        else:
            return jsonify({'error': 'Email already exists'}), 409
            
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Authenticate user
        user = db.authenticate_user(data['email'], data['password'])
        
        if user:
            # Generate token
            token = generate_token(user['id'], user['email'])
            
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': user
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/auth/profile', methods=['GET'])
@token_required
def get_profile():
    """Get user profile"""
    try:
        user_id = request.current_user['user_id']
        user = db.get_user_by_id(user_id)
        
        if user:
            return jsonify({'user': user}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        print(f"Profile error: {e}")
        return jsonify({'error': 'Failed to get profile'}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get products with optional filters"""
    try:
        # Get query parameters
        query = request.args.get('q')
        category = request.args.get('category')
        brand = request.args.get('brand')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        sort_by = request.args.get('sort', 'relevance')
        limit = request.args.get('limit', 8)
        
        # Convert numeric values
        if min_price is not None:
            min_price = float(min_price)
        if max_price is not None:
            max_price = float(max_price)
        if limit is not None:
            limit = int(limit)
        
        # Search products
        products = db.search_products(
            query=query,
            category=category,
            brand=brand,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by
        )
        
        # Apply limit if specified
        if limit:
            products = products[:limit]
        
        return jsonify({
            'products': products,
            'total': len(products)
        }), 200
        
    except Exception as e:
        print(f"Products error: {e}")
        return jsonify({'error': 'Failed to get products'}), 500

@app.route('/api/products/featured', methods=['GET'])
def get_featured_products():
    """Get featured products"""
    try:
        limit = request.args.get('limit', 8)
        
        # Convert numeric values
        if limit is not None:
            limit = int(limit)
        products = db.get_featured_products(limit)
        
        return jsonify({
            'products': products,
            'total': len(products)
        }), 200
        
    except Exception as e:
        print(f"Featured products error: {e}")
        return jsonify({'error': 'Failed to get featured products'}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get specific product details"""
    try:
        products = db.search_products()
        product = next((p for p in products if p['id'] == product_id), None)
        
        if product:
            return jsonify({'product': product}), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
            
    except Exception as e:
        print(f"Product error: {e}")
        return jsonify({'error': 'Failed to get product'}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        categories = db.get_categories()
        return jsonify({'categories': categories}), 200
        
    except Exception as e:
        print(f"Categories error: {e}")
        return jsonify({'error': 'Failed to get categories'}), 500

@app.route('/api/brands', methods=['GET'])
def get_brands():
    """Get all brands"""
    try:
        category = request.args.get('category')
        brands = db.get_brands(category)
        return jsonify({'brands': brands}), 200
        
    except Exception as e:
        print(f"Brands error: {e}")
        return jsonify({'error': 'Failed to get brands'}), 500

@app.route('/api/search', methods=['POST'])
def search_products():
    """Advanced product search"""
    try:
        data = request.get_json()
        
        query = data.get('query')
        category = data.get('category')
        brand = data.get('brand')
        min_price = data.get('min_price')
        max_price = data.get('max_price')
        sort_by = data.get('sort_by', 'relevance')
        
        # Convert numeric values
        if min_price is not None:
            min_price = float(min_price)
        if max_price is not None:
            max_price = float(max_price)
        
        products = db.search_products(
            query=query,
            category=category,
            brand=brand,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by
        )
        
        return jsonify({
            'products': products,
            'total': len(products),
            'query': query
        }), 200
        
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({'error': 'Search failed'}), 500

@app.route('/api/redirect/<int:product_id>/<string:retailer>', methods=['GET'])
def redirect_to_retailer(product_id, retailer):
    """Redirect to retailer with product URL"""
    try:
        products = db.search_products()
        product = next((p for p in products if p['id'] == product_id), None)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Get retailer URL
        retailer_urls = {
            'amazon': product.get('amazon_url'),
            'fnac': product.get('fnac_url'),
            'darty': product.get('darty_url'),
            'boulanger': product.get('boulanger_url'),
            'ldlc': product.get('ldlc_url'),
            'cdiscount': product.get('cdiscount_url')
        }
        
        url = retailer_urls.get(retailer.lower())
        
        if url:
            return jsonify({'redirect_url': url}), 200
        else:
            return jsonify({'error': 'Retailer not available for this product'}), 404
            
    except Exception as e:
        print(f"Redirect error: {e}")
        return jsonify({'error': 'Redirect failed'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize database with real products
    from models import init_real_products
    init_real_products()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
