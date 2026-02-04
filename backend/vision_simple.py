# Vision API SIMPLE et GARATUITE pour SmartChoice

import requests
import base64
import io
from PIL import Image
import json

class SimpleVision:
    def __init__(self):
        print("Vision simple initialisée...")
    
    def identify_object_basic(self, image_path):
        """Identification basique d'objets avec des mots-clés simples"""
        try:
            # Ouvrir l'image
            image = Image.open(image_path)
            
            # Analyse basique de l'image (couleurs dominantes, etc.)
            colors = image.getcolors(maxcolors=256*256*256)
            
            # Simulation de détection basée sur le nom du fichier
            filename = image_path.lower()
            
            # Mapping simple basé sur les noms de fichiers courants
            object_mapping = {
                'iphone': {'object': 'smartphone', 'keywords': ['telephone', 'apple', 'iphone']},
                'samsung': {'object': 'smartphone', 'keywords': ['telephone', 'samsung', 'galaxy']},
                'macbook': {'object': 'laptop', 'keywords': ['ordinateur', 'portable', 'apple']},
                'playstation': {'object': 'console', 'keywords': ['console', 'sony', 'ps5']},
                'xbox': {'object': 'console', 'keywords': ['console', 'microsoft', 'xbox']},
                'watch': {'object': 'montre', 'keywords': ['montre', 'apple watch']},
                'camera': {'object': 'camera', 'keywords': ['appareil photo', 'gopro']},
                'headphone': {'object': 'casque', 'keywords': ['casque', 'audio', 'sony']},
                'mouse': {'object': 'souris', 'keywords': ['souris', 'logitech']},
                'keyboard': {'object': 'clavier', 'keywords': ['clavier', 'logitech']},
                'monitor': {'object': 'ecran', 'keywords': ['ecran', 'samsung']},
                'tv': {'object': 'television', 'keywords': ['television', 'ecran']},
                'laptop': {'object': 'ordinateur', 'keywords': ['ordinateur', 'portable']},
                'computer': {'object': 'ordinateur', 'keywords': ['ordinateur', 'pc']},
                'gpu': {'object': 'carte graphique', 'keywords': ['carte graphique', 'nvidia']},
                'cpu': {'object': 'processeur', 'keywords': ['processeur', 'amd']},
            }
            
            # Chercher des correspondances
            detected_object = None
            keywords = []
            
            for key, value in object_mapping.items():
                if key in filename:
                    detected_object = value['object']
                    keywords = value['keywords']
                    break
            
            # Si rien n'est trouvé, utiliser une détection générique
            if not detected_object:
                detected_object = 'objet electronique'
                keywords = ['electronique', 'produit']
            
            return {
                'object': detected_object,
                'keywords': keywords,
                'confidence': 0.8,
                'source': 'simple_detection'
            }
            
        except Exception as e:
            print(f"Erreur détection simple: {e}")
            return {
                'object': 'objet inconnu',
                'keywords': ['produit'],
                'confidence': 0.5,
                'source': 'fallback'
            }
    
    def search_products_from_keywords(self, keywords):
        """Cherche des produits basés sur les mots-clés"""
        try:
            from models_fixed import DatabaseManager
            
            db = DatabaseManager()
            all_products = []
            
            for keyword in keywords:
                products = db.search_products(query=keyword)
                all_products.extend(products)
            
            # Éliminer les doublons
            unique_products = []
            seen_ids = set()
            
            for product in all_products:
                if product['id'] not in seen_ids:
                    unique_products.append(product)
                    seen_ids.add(product['id'])
            
            # Trier par pertinence
            unique_products.sort(key=lambda x: (x.get('featured', False), x.get('rating', 0)), reverse=True)
            
            return unique_products[:10]
            
        except Exception as e:
            print(f"Erreur recherche produits: {e}")
            return []
    
    def analyze_image_simple(self, image_path):
        """Analyse simple et rapide"""
        print(f"Analyse simple de: {image_path}")
        
        # Détection basique
        detection = self.identify_object_basic(image_path)
        
        # Recherche de produits
        products = self.search_products_from_keywords(detection['keywords'])
        
        return {
            'detection': detection,
            'similar_products': products,
            'total_products': len(products)
        }

# Test
if __name__ == "__main__":
    vision = SimpleVision()
    
    # Créer une fausse image pour tester
    try:
        # Test avec une image de test
        test_image = "test_product.jpg"
        
        # Si l'image n'existe pas, créer une image simple
        try:
            img = Image.new('RGB', (100, 100), color='red')
            img.save(test_image)
        except:
            pass
        
        result = vision.analyze_image_simple(test_image)
        
        print("\nRESULTATS SIMPLES:")
        print("=" * 40)
        print(f"Objet détecté: {result['detection']['object']}")
        print(f"Mots-clés: {result['detection']['keywords']}")
        print(f"Produits similaires: {result['total_products']}")
        
        for product in result['similar_products'][:3]:
            print(f"  - {product['name']} - {product['price']}€")
            
    except Exception as e:
        print(f"Erreur test: {e}")
