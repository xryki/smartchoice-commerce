@echo off
echo === DEPLOIEMENT AUTOMATIQUE ===

echo 1. Initialisation Git...
git init
git add .
git commit -m "Deploy SmartChoice"

echo 2. Connexion au repo GitHub...
git remote add origin https://github.com/TON_USERNAME/smartchoice-ecommerce.git
git branch -M main

echo 3. Upload sur GitHub...
git push -u origin main

echo 4. Ton site est prêt pour Render/Railway !
echo Va sur https://render.com/ ou https://railway.app/
echo Connecte ton repo et deploie !

pause
