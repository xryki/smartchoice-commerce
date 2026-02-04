# SmartChoice - E-commerce avec Intelligence Artificielle

Site e-commerce moderne construit avec Node.js, Express, MongoDB et une API de reconnaissance d'objets.

## 🚀 Fonctionnalités

- **Catalogue de produits** avec 9 produits de marques premium (Apple, Samsung, Sony, NVIDIA, AMD)
- **Recherche intelligente** par mots-clés avec mapping sémantique
- **API Vision GRATUITE** pour identifier des objets depuis des photos
- **Recherche de produits similaires** basée sur l'analyse d'images
- **Système d'authentification** JWT
- **Design responsive** moderne
- **Liens d'achat réels** vers Amazon, Fnac, Darty, LDLC

## 🛠️ Stack Technique

- **Backend**: Node.js, Express.js
- **Base de données**: MongoDB avec Mongoose
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Upload d'images**: Multer + Sharp
- **Authentification**: JWT
- **API Vision**: Analyse basique d'images (gratuite)

## 📦 Installation

1. Clonez le repository
```bash
git clone https://github.com/xryki/smartchoice-ecommerce.git
cd smartchoice-ecommerce
```

2. Installez les dépendances
```bash
npm install
```

3. Configurez les variables d'environnement
```bash
cp .env.example .env
# Éditez .env avec vos configurations
```

4. Lancez MongoDB
```bash
# Sur Windows avec MongoDB Community Server
# Sur Mac avec Homebrew: brew services start mongodb-community
# Sur Linux: sudo systemctl start mongod
```

5. Initialisez la base de données
```bash
node seed.js
```

6. Lancez le serveur
```bash
npm start
# ou en développement: npm run dev
```

## 🌐 Accès

- **Site**: http://localhost:5000
- **API Produits**: http://localhost:5000/api/products
- **API Vision**: http://localhost:5000/api/vision/identify

## 📱 Utilisation

### Recherche de produits
- Utilisez la barre de recherche avec des mots-clés intelligents
- Exemples: "montre", "telephone", "carte graphique", "processeur"

### API Vision
1. Cliquez sur "Scanner un produit"
2. Uploadez une photo d'un objet
3. L'IA identifie l'objet et trouve des produits similaires

### Mots-clés supportés
- `montre` → Apple Watch
- `telephone` → iPhone, Samsung Galaxy
- `ordinateur` → MacBook, ASUS, HP
- `console` → PlayStation 5
- `carte graphique` → NVIDIA RTX
- `processeur` → AMD Ryzen

## 🚀 Déploiement

### Railway (Recommandé)
1. Push sur GitHub
2. Connectez votre repo sur https://railway.app/
3. Ajoutez la variable d'environnement: `PORT=5000`
4. Déployez!

### Render
1. Push sur GitHub
2. Connectez votre repo sur https://render.com/
3. Configurez le build et start command
4. Déployez!

## 📁 Structure du Projet

```
smartchoice-ecommerce/
├── server.js              # Serveur principal
├── package.json           # Dépendances
├── .env                   # Variables d'environnement
├── seed.js                # Initialisation BDD
├── models/                # Modèles Mongoose
│   ├── Product.js
│   └── User.js
├── routes/                # Routes Express
│   ├── auth.js
│   ├── products.js
│   └── vision.js
├── data/                  # Données initiales
│   └── products.js
├── public/                # Frontend
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
└── README.md
```

## 🔧 API Endpoints

### Produits
- `GET /api/products` - Tous les produits
- `GET /api/products/featured` - Produits vedettes
- `POST /api/products/search` - Recherche avancée
- `GET /api/products/categories` - Catégories
- `GET /api/products/brands` - Marques

### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion
- `GET /api/auth/profile` - Profil utilisateur

### Vision
- `POST /api/vision/identify` - Identifier un objet depuis une image

## 🎯 Fonctionnalités Uniques

### API Vision Gratuite
- Analyse le nom de fichier de l'image
- Mapping intelligent vers des catégories de produits
- Recherche automatique de produits similaires
- Aucune dépendance externe requise

### Recherche Sémantique
- Mapping de mots-clés (ex: "montre" → "apple watch")
- Recherche multi-critères (nom, marque, description)
- Tri par pertinence, prix, notation

## 🛍️ Produits Disponibles

- **Apple**: iPhone 15 Pro Max, Apple Watch Series 10
- **Samsung**: Galaxy S24 Ultra, Odyssey G9 Monitor
- **Sony**: PlayStation 5 Slim
- **NVIDIA**: RTX 4090, RTX 4070 Ti
- **AMD**: Ryzen 9 7950X, Ryzen 7 7700X

## 📄 Licence

MIT License

## 🤝 Contributeurs

SmartChoice Team

---

**SmartChoice** - L'e-commerce du futur avec intelligence artificielle! 🚀
