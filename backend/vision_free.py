# Vision API 100% GRATUITE pour SmartChoice

import requests
import base64
import io
from PIL import Image
import json
import torch
from transformers import pipeline
import cv2
import numpy as np

class FreeObjectRecognition:
    def __init__(self):
        print("Chargement des modèles gratuits...")
        
        # Modèle Hugging Face (gratuit et puissant)
        try:
            self.detector = pipeline("object-detection", model="facebook/detr-resnet-50")
            print("Modèle Hugging Face charge")
        except Exception as e:
            print(f"Erreur Hugging Face: {e}")
            self.detector = None
        
        # Modèle de classification d'images
        try:
            self.classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
            print("Modèle de classification charge")
        except Exception as e:
            print(f"Erreur classification: {e}")
            self.classifier = None
    
    def identify_objects_free(self, image_path):
        """Identifie les objets gratuitement avec Hugging Face"""
        try:
            if not self.detector:
                return None
            
            image = Image.open(image_path)
            results = self.detector(image)
            
            objects = []
            for result in results:
                objects.append({
                    'object': result['label'],
                    'confidence': round(result['score'], 3),
                    'box': result['box']
                })
            
            return {
                'objects': objects,
                'source': 'huggingface_free',
                'total_objects': len(objects)
            }
            
        except Exception as e:
            print(f"Erreur identification: {e}")
            return None
    
    def classify_image_free(self, image_path):
        """Classifie l'image gratuitement"""
        try:
            if not self.classifier:
                return None
            
            image = Image.open(image_path)
            results = self.classifier(image)
            
            labels = []
            for result in results[:5]:  # Top 5 labels
                labels.append({
                    'label': result['label'],
                    'confidence': round(result['score'], 3)
                })
            
            return {
                'labels': labels,
                'source': 'huggingface_classifier'
            }
            
        except Exception as e:
            print(f"Erreur classification: {e}")
            return None
    
    def get_smart_keywords(self, object_info):
        """Génère des mots-clés intelligents pour la recherche"""
        keywords = []
        
        if object_info and 'objects' in object_info:
            for obj in object_info['objects']:
                obj_name = obj['object'].lower()
                confidence = obj['confidence']
                
                # Mots-clés directs
                keywords.append(obj_name)
                
                # Mapping intelligent vers des produits
                keyword_mapping = {
                    # Électronique
                    'cell phone': ['telephone', 'smartphone', 'iphone', 'samsung'],
                    'laptop': ['ordinateur', 'pc portable', 'macbook', 'asus'],
                    'computer': ['ordinateur', 'pc', 'desktop'],
                    'tv': ['television', 'ecran', 'monitor'],
                    'monitor': ['ecran', 'moniteur', 'samsung'],
                    'keyboard': ['clavier', 'logitech', 'razer'],
                    'mouse': ['souris', 'logitech', 'razer'],
                    'headphones': ['casque', 'audio', 'sony', 'bose'],
                    'camera': ['appareil photo', 'gopro', 'canon'],
                    
                    # Consoles de jeux
                    'game controller': ['console', 'playstation', 'xbox', 'nintendo'],
                    'remote': ['telecommande', 'console'],
                    
                    # Vêtements et accessoires
                    'watch': ['montre', 'apple watch', 'samsung'],
                    'handbag': ['sac', 'maroquinerie'],
                    'backpack': ['sac a dos'],
                    
                    # Maison
                    'bottle': ['bouteille', 'gourde'],
                    'cup': ['tasse', 'mug'],
                    'book': ['livre', 'kindle'],
                    
                    # Sports
                    'ball': ['ballon', 'sport'],
                    'bicycle': ['velo', 'cyclisme'],
                }
                
                # Ajouter les mots-clés mappés
                if obj_name in keyword_mapping:
                    keywords.extend(keyword_mapping[obj_name])
                
                # Ajouter des mots-clés basés sur la confiance
                if confidence > 0.8:
                    # Haute confiance - ajouter plus de variations
                    if 'phone' in obj_name:
                        keywords.extend(['mobile', 'portable'])
                    elif 'computer' in obj_name:
                        keywords.extend(['informatique', 'tech'])
        
        # Ajouter les labels de classification
        if object_info and isinstance(object_info, dict) and 'labels' in object_info:
            for label in object_info['labels']:
                label_name = label['label'].lower()
                if label['confidence'] > 0.7:
                    keywords.append(label_name)
        
        # Nettoyer et dédupliquer
        unique_keywords = list(set([kw.strip() for kw in keywords if len(kw.strip()) > 2]))
        
        return unique_keywords[:10]  # Limiter à 10 mots-clés
    
    def search_similar_products(self, object_info):
        """Cherche des produits similaires basés sur l'identification"""
        try:
            from models_fixed import DatabaseManager
            
            db = DatabaseManager()
            keywords = self.get_smart_keywords(object_info)
            
            print(f"Mots-clés de recherche: {keywords}")
            
            all_products = []
            for keyword in keywords:
                products = db.search_products(query=keyword)
                all_products.extend(products)
            
            # Éliminer les doublons et trier par pertinence
            unique_products = []
            seen_ids = set()
            
            for product in all_products:
                if product['id'] not in seen_ids:
                    unique_products.append(product)
                    seen_ids.add(product['id'])
            
            # Trier par rating et featured
            unique_products.sort(key=lambda x: (x.get('featured', False), x.get('rating', 0)), reverse=True)
            
            return unique_products[:12]  # Top 12 résultats
            
        except Exception as e:
            print(f"Erreur recherche produits: {e}")
            return []
    
    def analyze_image_complete(self, image_path):
        """Analyse complète de l'image avec toutes les méthodes gratuites"""
        print(f"Analyse de l'image: {image_path}")
        
        results = {
            'objects': self.identify_objects_free(image_path),
            'classification': self.classify_image_free(image_path),
            'similar_products': []
        }
        
        # Combiner les résultats pour la recherche
        combined_info = {}
        if results['objects']:
            combined_info.update(results['objects'])
        if results['classification']:
            combined_info.update(results['classification'])
        
        # Chercher des produits similaires
        if combined_info:
            results['similar_products'] = self.search_similar_products(combined_info)
        
        return results

# Test rapide
if __name__ == "__main__":
    vision = FreeObjectRecognition()
    
    # Test avec une image (remplace avec ton chemin)
    image_path = "test_image.jpg"
    
    try:
        results = vision.analyze_image_complete(image_path)
        
        print("\nRESULTATS DE L'ANALYSE:")
        print("=" * 50)
        
        if results['objects']:
            print(f"Objets détectés: {results['objects']['total_objects']}")
            for obj in results['objects']['objects'][:5]:
                print(f"  - {obj['object']} (confiance: {obj['confidence']})")
        
        if results['classification']:
            print(f"\nClassification:")
            for label in results['classification']['labels'][:3]:
                print(f"  - {label['label']} (confiance: {label['confidence']})")
        
        if results['similar_products']:
            print(f"\nProduits similaires trouvés: {len(results['similar_products'])}")
            for product in results['similar_products'][:3]:
                print(f"  - {product['name']} - {product['price']}€ ({product['brand']})")
        
    except Exception as e:
        print(f"Erreur: {e}")
        print("Assure-toi d'avoir une image 'test_image.jpg' dans le dossier")
