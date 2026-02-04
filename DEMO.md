# SmartChoice - Guide de Démonstration

## Lancement de l'Application

L'application est déjà en cours d'exécution sur `http://localhost:5000`

## Scénarios de Test

### Scénario 1: Recherche d'un Smartphone (Classe Moyenne)
**Paramètres:**
- Budget: 1000€
- Classe sociale: Moyenne
- Produit: "iPhone"
- Catégorie: Électronique

**Résultats attendus:**
- iPhone 15 Pro trouvé (1199€ - légèrement au-dessus du budget)
- Recommandation personnalisée avec explication
- Analyse qualité exceptionnelle et vendeur fiable

### Scénario 2: Recherche de Vêtements (Classe Faible)
**Paramètres:**
- Budget: 100€
- Classe sociale: Faible
- Produit: "Jean"
- Catégorie: Vêtements

**Résultats attendus:**
- Levi's 501 trouvé (89€ - dans le budget)
- Recommandation basée sur le meilleur rapport qualité-prix
- Priorité accordée au prix

### Scénario 3: Recherche Multi-catégories
**Paramètres:**
- Budget: 500€
- Classe sociale: Élevée
- Produit: "Pro"
- Catégorie: Électronique

**Résultats attendus:**
- MacBook Air M2 trouvé (1299€ - au-dessus du budget)
- Recommandation axée sur la qualité maximale
- Moins d'importance sur le prix

## Points Clés à Démontrer

### 1. Algorithme Intelligent
- **Pondération adaptative** selon la classe sociale
- **Analyse multi-critères** (prix, qualité, fiabilité)
- **Explications transparentes** des recommandations

### 2. Interface Utilisateur
- **Design moderne et responsive**
- **Navigation intuitive**
- **Affichage clair des résultats**

### 3. Sécurité et Fiabilité
- **Filtrage des sites peu fiables** (seuil 60%)
- **Validation des entrées utilisateur**
- **Protection contre les arnaques**

## Données de Test

### Base de Données
- **12 produits** répartis en 4 catégories
- **Marques variées**: Apple, Samsung, Nike, Levi's, etc.
- **Scores réalistes**: qualité (70-96), fiabilité (78-100)

### Catégories Disponibles
- **Électronique**: iPhone, Galaxy, MacBook, ThinkPad
- **Vêtements**: Levi's, Vans, Nike
- **Maison**: Roomba, Nespresso
- **Sports**: Tapis yoga, Chaussures running

## Messages Clés pour la Présentation

### Innovation
- "Intégration unique du critère **classe sociale** dans la recommandation"
- "Algorithme **transparent et explicable**"
- "Protection active contre les **sites peu fiables**"

### Problèmes Résolus
- "Évite les **arnaques** en filtrant les vendeurs"
- "**Adapte** les recommandations au budget réel"
- "**Simplifie** la décision face à des produits similaires"

### Impact
- "**Accessible** à tous les budgets"
- "**Personnalisé** selon le profil utilisateur"
- "**Sécurisé** grâce à l'analyse de fiabilité"

## Démo Live

1. **Navigation**: Montrer l'interface d'accueil
2. **Recherche**: Effectuer une recherche en direct
3. **Résultats**: Expliquer les différentes recommandations
4. **Personnalisation**: Montrer l'impact de la classe sociale
5. **Filtrage**: Démontrer le tri par marque/prix/qualité

## Questions Fréquentes

**Q: Comment l'algorithme détermine-t-il la fiabilité?**
R: Basé sur un score de 0-100 évaluant la réputation du vendeur

**Q: Les données sont-elles en temps réel?**
R: Pour la démo, utilise une base de données statique. En production, pourrait s'connecter à des APIs externes

**Q: Comment évolue le système?**
R: L'algorithme apprend des préférences utilisateur et s'adapte aux nouvelles données

---

*SmartChoice - L'achat intelligent devient simple*
