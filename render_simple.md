# Render - DEPLOIEMENT ULTRA-SIMPLE

## ÉTAPE 1: Crée un compte Render (30 secondes)
1. Va sur https://render.com/
2. "Sign up" → "Sign up with GitHub"
3. Autorise Render à accéder à tes repos

## ÉTAPE 2: Crée le Web Service (1 minute)
1. Sur le dashboard Render, clique "New +"
2. Clique "Web Service"
3. Sélectionne ton repo `smartchoice-ecommerce`
4. Render va détecter automatiquement Python

## ÉTAPE 3: Configuration (30 secondes)
Remplis les champs :
- **Name**: `smartchoice-ecommerce`
- **Runtime**: `Python 3` (déjà sélectionné)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app_clean.py`
- **Instance Type**: `Free`

## ÉTAPE 4: Variables d'environnement (10 secondes)
1. Clique "Advanced" → "Add Environment Variable"
2. Ajoute: `PYTHONPATH` = `/app`
3. Clique "Add Variable"

## ÉTAPE 5: Déploie !
Clique "Create Web Service"

## FINI ! 🎉

Render va :
- ✅ Installer automatiquement tes dépendances
- ✅ Lancer ton application Flask
- ✅ Te donner une URL HTTPS
- ✅ Configurer un certificat SSL
- ✅ Surveiller ton application

## TON URL SERA :
https://smartchoice-ecommerce.onrender.com

---

## AVANTAGES DE RENDER :
✅ Plus rapide que Railway
✅ Interface plus simple
✅ Déploiement automatique
✅ URL plus propre
✅ Monitoring inclus
✅ 750h/mois gratuit

## SI ÇA MARCHE PAS :
- Vérifie que tes 6 fichiers sont bien sur GitHub
- Le Build Command doit être exactement: `pip install -r requirements.txt`
- Le Start Command doit être exactement: `python app_clean.py`

C'EST TOUT ! Render fait le reste automatiquement !
