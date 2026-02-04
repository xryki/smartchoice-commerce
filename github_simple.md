# GitHub SIMPLIFIÉ pour SmartChoice

## ÉTAPE 1: Crée un compte (2 minutes)
1. Va sur https://github.com/
2. "Sign up" → Utilise ton email
3. Vérifie ton email

## ÉTAPE 2: Crée le repo (30 secondes)
1. Clique sur le "+" en haut à droite
2. "New repository"
3. Remplis:
   - Repository name: `smartchoice-ecommerce`
   - Description: `Site e-commerce avec vision AI`
   - Public (coche)
   - NE coche PAS "Add a README"
4. Clique "Create repository"

## ÉTAPE 3: Upload tes fichiers (1 minute)
1. Sur la page du repo, clique "uploading an existing file"
2. Glisse-dépose ces 5 fichiers:
   - `backend/app_clean.py`
   - `backend/models_fixed.py`
   - `backend/vision_simple.py`
   - `backend/requirements.txt`
   - `backend/products_part1.py`
   - `backend/products_part2_clean.py`
3. En bas, mets "Commit changes"
4. Clique "Commit changes"

## ÉTAPE 4: Copie l'URL du repo (5 secondes)
1. Sur ton repo, clique le bouton vert "Code"
2. Copie l'URL HTTPS
3. Exemple: `https://github.com/tonpseudo/smartchoice-ecommerce.git`

## ÉTAPE 5: Va sur Railway
1. Va sur https://railway.app/
2. "Sign up with GitHub"
3. "New Project" → "Deploy from GitHub repo"
4. Sélectionne `smartchoice-ecommerce`
5. Configure:
   - Name: `smartchoice`
   - Environment Variables: `PORT=5000`
6. Clique "Deploy"

## FINI ! 
Ton site sera sur: https://smartchoice-production.up.railway.app

---

## RAPPEL - FICHIERS À UPLOADER (5 fichiers seulement)
```
backend/
├── app_clean.py              ✅
├── models_fixed.py           ✅  
├── vision_simple.py          ✅
├── requirements.txt          ✅
├── products_part1.py         ✅
└── products_part2_clean.py   ✅
```

C'EST TOUT ! Le reste n'est pas nécessaire pour le déploiement.
