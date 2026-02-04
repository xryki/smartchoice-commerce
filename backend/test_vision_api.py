# Test de l'API Vision GRATUITE

import requests
import json

def test_vision_api():
    """Test l'API de reconnaissance d'objets"""
    
    base_url = "http://localhost:5000"
    
    print("Test de l'API Vision GRATUITE")
    print("=" * 50)
    
    # Test 1: Upload d'une image (simulation)
    print("\nTest 1: Upload d'image")
    
    # Créer une fausse image pour le test
    try:
        import io
        from PIL import Image
        
        # Créer une image simple
        img = Image.new('RGB', (100, 100), color='blue')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        # Envoyer l'image
        files = {'image': ('test_iphone.jpg', img_bytes, 'image/jpeg')}
        
        response = requests.post(f"{base_url}/api/vision/identify", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("API Vision fonctionne!")
            print(f"   Objet détecté: {data['detection']['object']}")
            print(f"   Mots-clés: {data['detection']['keywords']}")
            print(f"   Produits similaires: {data['total_products']}")
            
            # Afficher les produits trouvés
            for i, product in enumerate(data['similar_products'][:3]):
                print(f"   {i+1}. {product['name']} - {product['price']}€ ({product['brand']})")
        else:
            print(f"Erreur API Vision: {response.status_code}")
            print(f"   Message: {response.text}")
            
    except Exception as e:
        print(f"Erreur test: {e}")
    
    # Test 2: Vérifier que l'API search fonctionne toujours
    print("\nTest 2: API Search normale")
    
    try:
        response = requests.post(
            f"{base_url}/api/search",
            json={"query": "iphone"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("API Search fonctionne!")
            print(f"   Produits trouvés: {data['total']}")
            
            for i, product in enumerate(data['products'][:3]):
                print(f"   {i+1}. {product['name']} - {product['price']}€")
        else:
            print(f"Erreur API Search: {response.status_code}")
            
    except Exception as e:
        print(f"Erreur test search: {e}")
    
    # Test 3: Vérifier les produits vedettes
    print("\nTest 3: Produits vedettes")
    
    try:
        response = requests.get(f"{base_url}/api/products/featured")
        
        if response.status_code == 200:
            data = response.json()
            print("API Featured fonctionne!")
            print(f"   Produits vedettes: {data['total']}")
        else:
            print(f"Erreur API Featured: {response.status_code}")
            
    except Exception as e:
        print(f"Erreur test featured: {e}")

if __name__ == "__main__":
    test_vision_api()
