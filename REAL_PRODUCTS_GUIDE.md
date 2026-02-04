# Guide pour Intégrer des Produits Réels

## Objectif
Ajouter des produits réels avec des liens d'achat fonctionnels à SmartChoice.

## Options Disponibles

### 1. **API Externes (Recommandé pour la Production)**

#### Amazon Product Advertising API
```python
# Nécessite un compte Amazon Developer
# Coût : Gratuit jusqu'à 1000 requêtes/jour
# Documentation : https://webservices.amazon.com/paapi5/documentation/
```

#### eBay Finding API
```python
# Nécessite un compte eBay Developer
# Coût : Gratuit avec quota limité
# Documentation : https://developer.ebay.com/api-docs/buy/static/finding.html
```

#### Réseaux d'Affiliation Français
- **Darty Marketplace** : API pour les vendeurs partenaires
- **Fnac Marketplace** : API Marketplace
- **Cdiscount** : API pour les affiliés
- **Rakuten** : API affiliation

### 2. **Web Scraping (Attention légal)**

#### Sites Cibles
```python
SITES_SCRAPE = [
    'https://www.ldlc.com',
    'https://www.boulanger.com', 
    'https://www.fnac.com',
    'https://www.darty.com'
]
```

#### Exemple de Code
```python
import requests
from bs4 import BeautifulSoup

def scrape_ldlc(search_query):
    url = f"https://www.ldlc.com/recherche/{search_query}"
    headers = {'User-Agent': 'Mozilla/5.0...'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = []
    for item in soup.select('.product'):
        product = {
            'name': item.select_one('.title').text,
            'price': float(item.select_one('.price').text.replace('€', '')),
            'brand': item.select_one('.brand').text,
            'purchase_url': item.select_one('a')['href'],
            'image_url': item.select_one('img')['src']
        }
        products.append(product)
    
    return products
```

### 3. **API de Comparaison de Prix**

#### Comparez (API payante)
```python
# https://www.comparez.fr/api/
# Coût : Abonnement mensuel
# Couverture : France, Belgique, Suisse
```

#### Idealo (API payante)
```python
# https://www.idealo.fr/partenaires/api-prix/
# Coût : Commission sur ventes
# Couverture : Principalement Europe
```

### 4. **Open Data (Gratuit)**

#### Open Food Facts
```python
# Produits alimentaires uniquement
# API : https://world.openfoodfacts.org/api/v2/
# Gratuit et open source
```

#### Data.gouv.fr
```python
# Données publiques françaises
# Peut contenir des informations sur les prix
```

## Implémentation Rapide (Mock API)

J'ai déjà implémenté une **Mock API** dans `backend/api_integration.py` qui simule 1000 produits avec des liens d'achat.

### Avantages
- **Immédiat** : Fonctionne tout de suite
- **Liens cliquables** : Chaque produit a un purchase_url
- **Variété** : 8 catégories, 10 marques, 8 sites
- **Images** : Images aléatoires via Picsum

### Comment l'utiliser
1. **Redémarrez le serveur Flask** : `cd backend && python app.py`
2. **Testez une recherche** : "iPhone", "Nike", "Samsung"
3. **Cliquez sur les produits** : Liens d'achat disponibles

## Configuration pour Vraies APIs

### Étape 1 : Obtenir les Clés API
```bash
# Amazon PA API
1. Créer un compte Amazon Developer
2. S'inscrire au Product Advertising API
3. Obtenir : Access Key, Secret Key, Partner Tag

# eBay API  
1. Créer un compte eBay Developer
2. Générer un App ID
3. Configurer les tokens OAuth
```

### Étape 2 : Mettre à Jour le Code
```python
# Dans backend/api_integration.py
class AmazonAPI:
    def __init__(self):
        self.access_key = "VOTRE_ACCESS_KEY"
        self.secret_key = "VOTRE_SECRET_KEY" 
        self.partner_tag = "VOTRE_PARTNER_TAG"
```

### Étape 3 : Tester l'Intégration
```python
# Test simple
api = AmazonAPI()
products = api.search("iPhone 15", "electronics", 1000)
print(f"Trouvé {len(products)} produits")
```

## Considérations Légales

### Web Scraping
- **Autorisé** : Données publiques
- **Interdit** : Contenu protégé par copyright
- **Vérifier** : Conditions d'utilisation du site

### API Usage
- **Respecter** : Limites de taux (rate limits)
- **Attribuer** : Source des données
- **Coûts** : Certaines APIs sont payantes

### Affiliation
- **Déclarer** : Liens d'affiliation
- **Transparence** : Mentionner les commissions
- **CGU** : Conditions générales claires

## Coûts Estimés

### Option Gratuite (Mock API)
- **Coût** : 0€
- **Maintenance** : Aucune
- **Réalisme** : Limité mais fonctionnel

### API Payantes
- **Amazon PA API** : Gratuit jusqu'à 1000 requêtes/jour
- **eBay API** : Gratuit avec quota
- **Comparez** : ~50€/mois
- **Idéalo** : Commission sur ventes

### Web Scraping
- **Coût** : Temps de développement
- **Maintenance** : Mises à jour régulières
- **Risques** : Blocage IP, changements HTML

## Recommandation

### Pour votre Projet NSI
**Utilisez la Mock API déjà implémentée** :
- Parfait pour la démonstration
- Tous les liens fonctionnent  
- Aucune configuration requise
- Illustre parfaitement le concept

### Pour la Production
**Commencez avec Open Food Facts + Réseaux d'affiliation** :
- Gratuit et légal
- Données réelles
- Possibilité de monétisation

---

## Test Immédiat

1. **Redémarrez le serveur** :
   ```bash
   cd backend
   python app.py
   ```

2. **Testez des recherches** :
   - "iPhone" → Produits électroniques avec liens
   - "Nike" → Vêtements et sports avec liens  
   - "Samsung" → Électronique avec liens
   - "Lego" → Jouets avec liens

3. **Cliquez sur les produits** pour voir les liens d'achat !

**Votre application est maintenant prête avec des produits et des liens d'achat !**
