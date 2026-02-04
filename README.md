# SmartChoice - Assistant d'Achat Intelligent

SmartChoice est une plateforme web intelligente destinée à aider les utilisateurs à choisir le produit le plus adapté à leur budget, leur classe sociale et la fiabilité du site vendeur.

## Objectifs

- Faciliter la prise de décision lors d'un achat en ligne
- Protéger les utilisateurs contre les arnaques et les sites peu fiables
- Proposer des recommandations adaptées au profil financier de l'utilisateur
- Offrir une interface simple, intuitive et accessible
- Développer un algorithme de recommandation multi-critères

## Architecture

### Frontend
- **HTML5** : Structure sémantique
- **CSS3** : Design responsive avec variables CSS
- **JavaScript** : Interactions et appels API

### Backend
- **Python Flask** : Serveur web et API REST
- **SQLite** : Base de données légère
- **Algorithme personnalisé** : Système de recommandation

## 📁 Structure du Projet

```
smart choice/
├── frontend/                 # Fichiers frontend
│   ├── index.html           # Page d'accueil
│   └── results.html         # Page de résultats
├── backend/                 # Code backend
│   ├── app.py              # Application Flask principale
│   └── recommender.py      # Algorithme de recommandation
├── database/               # Base de données
│   └── models.py           # Modèles et initialisation
├── static/                 # Fichiers statiques
│   ├── css/
│   │   └── styles.css      # Styles principaux
│   └── js/
│       ├── script.js       # JavaScript page d'accueil
│       └── results.js      # JavaScript page résultats
├── requirements.txt        # Dépendances Python
└── README.md              # Documentation
```

## Installation et Démarrage

### Prérequis
- Python 3.8 ou supérieur
- npm (optionnel, pour le développement)

### Étapes d'installation

1. **Cloner le projet**
   ```bash
   git clone <repository-url>
   cd "smart choice"
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialiser la base de données**
   ```bash
   cd database
   python models.py
   cd ..
   ```

5. **Démarrer l'application**
   ```bash
   cd backend
   python app.py
   ```

6. **Accéder à l'application**
   Ouvrez votre navigateur et allez sur : `http://localhost:5000`

## Fonctionnalités

### Fonctionnalités Principales
- **Formulaire utilisateur** : Budget, classe sociale, produit, catégorie
- **Recherche intelligente** : Analyse multi-critères des produits
- **Comparaison des prix** : Trouver les meilleures offres
- **Analyse de qualité** : Évaluation basée sur les notes et caractéristiques
- **Fiabilité des vendeurs** : Filtrage des sites fiables
- **Recommandations personnalisées** : Adaptées au profil utilisateur

### Types de Recommandations
- **Le moins cher** : Meilleur prix dans le budget
- **Le plus fiable** : Vendeur le plus trustworthy
- **Meilleure qualité** : Produit avec le meilleur score qualité
- **Recommandation personnalisée** : Basée sur l'algorithme SmartChoice

### Fonctionnalités Secondaires
- **Filtrage par marque** : Affiner les recherches
- **Tri multi-critères** : Prix, qualité, fiabilité, score global
- **Design responsive** : Compatible mobile/desktop
- **Interface moderne** : Design épuré et intuitif

## Algorithme de Recommandation

L'algorithme SmartChoice analyse plusieurs critères :

### Critères Évalués
1. **Prix** : Rapport qualité-prix
2. **Qualité** : Score basé sur les avis et caractéristiques
3. **Fiabilité** : Confiance dans le vendeur
4. **Budget utilisateur** : Respect des contraintes financières
5. **Classe sociale** : Pondération personnalisée

### Pondération par Classe Sociale
- **Classe faible** : 50% prix, 20% qualité, 30% fiabilité
- **Classe moyenne** : 30% prix, 40% qualité, 30% fiabilité  
- **Classe élevée** : 10% prix, 50% qualité, 40% fiabilité

### Score Global
Le score global est calculé selon la formule :
```
Score = (poids_prix × score_prix) + 
        (poids_qualité × score_qualité) + 
        (poids_fiabilité × score_fiabilité)
```

## API Endpoints

### Recherche de produits
```
POST /api/search
Content-Type: application/json

{
    "budget": 1000,
    "social_class": "medium",
    "product": "iPhone",
    "category": "electronics"
}
```

### Récupérer tous les produits
```
GET /api/products?category=electronics
```

### Catégories disponibles
```
GET /api/categories
```

### Marques disponibles
```
GET /api/brands?category=electronics
```

## Base de Données

### Table Products
| Champ | Type | Description |
|-------|------|-------------|
| id | INTEGER | ID unique |
| name | TEXT | Nom du produit |
| category | TEXT | Catégorie |
| brand | TEXT | Marque |
| price | REAL | Prix en euros |
| rating | REAL | Note moyenne |
| quality_score | INTEGER | Score qualité (0-100) |
| site | TEXT | Site vendeur |
| site_reliability | INTEGER | Fiabilité site (0-100) |

## Design et UX

### Principes de Design
- **Clarté** : Information hiérarchisée et lisible
- **Accessibilité** : Interface intuitive pour tous
- **Responsive** : Adaptation mobile/tablette/desktop
- **Performance** : Chargement rapide et interactions fluides

### Couleurs et Thème
- **Primaire** : Bleu trust (#2563eb)
- **Secondaire** : Vert succès (#10b981)
- **Accent** : Orange action (#f59e0b)
- **Neutres** : Gris modernes pour le texte et fonds

## 🧪 Tests

### Tests Manuel
1. **Test de recherche** : Vérifier les résultats de recherche
2. **Test de recommandations** : Valider l'algorithme
3. **Test responsive** : Vérifier l'affichage mobile
4. **Test performance** : Mesurer les temps de réponse

### Tests Automatisés (futur)
```bash
# Tests unitaires
python -m pytest tests/

# Tests d'intégration
python -m pytest tests/integration/
```

## Améliorations Futures

### Court Terme
- [ ] Ajouter plus de produits dans la base
- [ ] Améliorer l'algorithme de recommandation
- [ ] Ajouter des filtres avancés
- [ ] Historique des recherches

### Moyen Terme
- [ ] Comptes utilisateurs et préférences
- [ ] Alertes de prix
- [ ] Comparaison en temps réel
- [ ] API externes (Amazon, etc.)

### Long Terme
- [ ] Machine Learning pour les recommandations
- [ ] Application mobile native
- [ ] Analyse des tendances
- [ ] Communauté et avis

## 🤝 Contribuer

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est réalisé dans le cadre d'un projet NSI (Numérique et Sciences Informatiques).

## 👥 Équipe

- **Développeur principal** : [Votre nom]
- **Encadrant** : [Nom de l'encadrant]
- **Établissement** : [Votre établissement]

## 📞 Contact

Pour toute question ou suggestion :
- Email : [votre.email@example.com]
- Projet GitHub : [lien vers le repository]

---

**SmartChoice** - Votre assistant d'achat intelligent
