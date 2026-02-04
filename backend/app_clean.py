# Clean Flask app with all products

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import jwt
import datetime
from functools import wraps
import os
import base64

from models_fixed import DatabaseManager
from vision_simple import SimpleVision

app = Flask(__name__, static_folder='../static', template_folder='../frontend')
CORS(app)

# JWT Configuration
app.config['SECRET_KEY'] = 'smartchoice-secret-key-2024'

# Initialize database
db = DatabaseManager()

# Initialize vision
vision = SimpleVision()

# JWT Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = db.get_user_by_email(data['email'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
        except:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# Routes
@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/products')
def products():
    """Serve the products page"""
    return render_template('products.html')

@app.route('/login')
def login_page():
    """Serve the login page"""
    return render_template('login.html')

@app.route('/register')
def register_page():
    """Serve the registration page"""
    return render_template('register.html')

# API Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration"""
    try:
        data = request.get_json()
        
        # Check if user already exists
        existing_user = db.get_user_by_email(data['email'])
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400
        
        # Create new user
        user_id = db.add_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data.get('age'),
            phone=data.get('phone')
        )
        
        # Generate token
        token = jwt.encode({
            'email': data['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        
        # Get user data
        user = db.get_user_by_email(data['email'])
        
        return jsonify({
            'message': 'User created successfully',
            'user': {
                'id': user['id'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name']
            },
            'token': token
        }), 201
        
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login_user():
    """User login"""
    try:
        data = request.get_json()
        
        # Get user
        user = db.get_user_by_email(data['email'])
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check password (in production, use proper hashing)
        import hashlib
        password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
        
        if user['password_hash'] != password_hash:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate token
        token = jwt.encode({
            'email': user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name']
            },
            'token': token
        }), 200
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/auth/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get user profile"""
    try:
        return jsonify({
            'user': {
                'id': current_user['id'],
                'email': current_user['email'],
                'first_name': current_user['first_name'],
                'last_name': current_user['last_name'],
                'age': current_user['age'],
                'phone': current_user['phone']
            }
        }), 200
        
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

@app.route('/api/vision/identify', methods=['POST'])
def identify_object():
    """Identify object from uploaded image - GRATUIT"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image file provided'}), 400
        
        # Save temporary image
        temp_path = f"temp_{file.filename}"
        file.save(temp_path)
        
        # Analyze with simple vision
        result = vision.analyze_image_simple(temp_path)
        
        # Clean up
        import os
        try:
            os.remove(temp_path)
        except:
            pass
        
        return jsonify({
            'success': True,
            'detection': result['detection'],
            'similar_products': result['similar_products'],
            'total_products': result['total_products']
        }), 200
        
    except Exception as e:
        print(f"Vision error: {e}")
        return jsonify({'error': 'Object identification failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
