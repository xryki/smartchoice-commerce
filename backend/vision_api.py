# Vision API integration for SmartChoice

import requests
import base64
import io
from PIL import Image
import json

class ObjectRecognition:
    def __init__(self):
        self.google_api_key = "YOUR_GOOGLE_VISION_API_KEY"
        self.openai_api_key = "YOUR_OPENAI_API_KEY"
    
    def identify_object_google(self, image_path):
        """Identify objects using Google Vision API"""
        try:
            # Convert image to base64
            with open(image_path, 'rb') as image_file:
                image_content = base64.b64encode(image_file.read()).decode()
            
            # Google Vision API request
            url = f"https://vision.googleapis.com/v1/images:annotate?key={self.google_api_key}"
            
            payload = {
                "requests": [
                    {
                        "image": {
                            "content": image_content
                        },
                        "features": [
                            {"type": "LABEL_DETECTION", "maxResults": 10},
                            {"type": "OBJECT_LOCALIZATION", "maxResults": 10},
                            {"type": "WEB_DETECTION", "maxResults": 10}
                        ]
                    }
                ]
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return self.parse_google_response(result)
            else:
                print(f"Google Vision API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error with Google Vision: {e}")
            return None
    
    def identify_object_openai(self, image_path):
        """Identify objects using OpenAI Vision API"""
        try:
            # Convert image to base64
            with open(image_path, 'rb') as image_file:
                image_content = base64.b64encode(image_file.read()).decode()
            
            # OpenAI Vision API request
            url = "https://api.openai.com/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Identifie précisément cet objet et donne-moi:
1. Le nom exact de l'objet
2. La marque si visible
3. Le modèle si visible
4. La catégorie (électronique, vêtement, alimentation, etc.)
5. Des mots-clés pour trouver des produits similaires

Réponds en format JSON."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_content}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 500
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return self.parse_openai_response(result)
            else:
                print(f"OpenAI Vision API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error with OpenAI Vision: {e}")
            return None
    
    def parse_google_response(self, response):
        """Parse Google Vision API response"""
        try:
            labels = []
            objects = []
            web_entities = []
            
            # Extract labels
            if 'labelAnnotations' in response['responses'][0]:
                for label in response['responses'][0]['labelAnnotations']:
                    labels.append({
                        'name': label['description'],
                        'confidence': label['score']
                    })
            
            # Extract objects
            if 'localizedObjectAnnotations' in response['responses'][0]:
                for obj in response['responses'][0]['localizedObjectAnnotations']:
                    objects.append({
                        'name': obj['name'],
                        'confidence': obj['score']
                    })
            
            # Extract web entities
            if 'webDetection' in response['responses'][0]:
                if 'webEntities' in response['responses'][0]['webDetection']:
                    for entity in response['responses'][0]['webDetection']['webEntities']:
                        if 'description' in entity:
                            web_entities.append({
                                'name': entity['description'],
                                'confidence': entity.get('score', 0)
                            })
            
            return {
                'labels': labels,
                'objects': objects,
                'web_entities': web_entities,
                'source': 'google_vision'
            }
            
        except Exception as e:
            print(f"Error parsing Google response: {e}")
            return None
    
    def parse_openai_response(self, response):
        """Parse OpenAI Vision API response"""
        try:
            content = response['choices'][0]['message']['content']
            
            # Try to parse JSON from the response
            try:
                return json.loads(content)
            except:
                # If not JSON, return as text
                return {
                    'text_response': content,
                    'source': 'openai_vision'
                }
                
        except Exception as e:
            print(f"Error parsing OpenAI response: {e}")
            return None
    
    def search_similar_products(self, object_info):
        """Search for similar products based on object identification"""
        from models_fixed import DatabaseManager
        
        db = DatabaseManager()
        
        # Extract keywords from object info
        keywords = []
        
        if isinstance(object_info, dict):
            if 'labels' in object_info:
                keywords.extend([label['name'] for label in object_info['labels']])
            if 'objects' in object_info:
                keywords.extend([obj['name'] for obj in object_info['objects']])
            if 'web_entities' in object_info:
                keywords.extend([entity['name'] for entity in object_info['web_entities']])
        
        # Search products using keywords
        all_products = []
        for keyword in keywords[:5]:  # Limit to first 5 keywords
            products = db.search_products(query=keyword)
            all_products.extend(products)
        
        # Remove duplicates and sort by relevance
        unique_products = []
        seen_ids = set()
        
        for product in all_products:
            if product['id'] not in seen_ids:
                unique_products.append(product)
                seen_ids.add(product['id'])
        
        return unique_products[:10]  # Return top 10 results

# Flask route for image upload and object recognition
def add_vision_routes(app):
    """Add vision API routes to Flask app"""
    
    @app.route('/api/vision/identify', methods=['POST'])
    def identify_object():
        """Identify object from uploaded image"""
        try:
            if 'image' not in request.files:
                return jsonify({'error': 'No image file provided'}), 400
            
            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'No image file provided'}), 400
            
            # Save temporary image
            temp_path = f"temp_{file.filename}"
            file.save(temp_path)
            
            # Initialize object recognition
            vision = ObjectRecognition()
            
            # Try Google Vision first, then OpenAI
            result = vision.identify_object_google(temp_path)
            if not result:
                result = vision.identify_object_openai(temp_path)
            
            # Clean up temporary file
            import os
            os.remove(temp_path)
            
            if result:
                # Search for similar products
                similar_products = vision.search_similar_products(result)
                
                return jsonify({
                    'object_info': result,
                    'similar_products': similar_products,
                    'total_products': len(similar_products)
                }), 200
            else:
                return jsonify({'error': 'Failed to identify object'}), 500
                
        except Exception as e:
            print(f"Vision API error: {e}")
            return jsonify({'error': 'Object identification failed'}), 500

# Usage example
if __name__ == "__main__":
    vision = ObjectRecognition()
    
    # Test with an image
    result = vision.identify_object_google("test_image.jpg")
    if result:
        print("Object identified:", result)
        
        # Search for similar products
        products = vision.search_similar_products(result)
        print(f"Found {len(products)} similar products")
