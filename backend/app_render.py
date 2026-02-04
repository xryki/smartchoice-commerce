# Version optimisée pour Render

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

# Configuration pour Render
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'smartchoice-secret-key-2024')
PORT = int(os.environ.get('PORT', 5000))

# Initialize database
db = DatabaseManager()

# Initialize vision
vision = SimpleVision()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products_page():
    return render_template('products.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

# API Routes
@app.route('/api/auth/register', methods=['POST'])
def register_page_api():
    """Register new user"""
    try:
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        age = data.get('age')
        phone = data.get('phone')
        
        # Check if user already exists
        existing_user = db.get_user_by_email(email)
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400
        
        # Create new user
        user_id = db.add_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            age=age,
            phone=phone
        )
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user_id': user_id
        }), 201
        
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login_user():
    """Login user"""
    try:
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        
        # Get user from database
        user = db.get_user_by_email(email)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check password (simplified - in production use proper hashing)
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if user['password_hash'] != password_hash:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name']
            }
        }), 200
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        products = db.search_products()
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
        products = db.get_featured_products()
        return jsonify({
            'products': products,
            'total': len(products)
        }), 200
        
    except Exception as e:
        print(f"Featured products error: {e}")
        return jsonify({'error': 'Failed to get featured products'}), 500

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

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
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

@app.route('/health')
def health_check():
    """Health check for Render"""
    return jsonify({'status': 'healthy', 'port': PORT}), 200

if __name__ == '__main__':
    print("Démarrage pour Render...")
    print(f"Port: {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
