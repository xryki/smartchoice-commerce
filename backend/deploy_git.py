# Déploiement avec Git (le plus simple dans le terminal)

import subprocess
import sys
import os

def deploy_with_git():
    """Déploie en utilisant Git directement"""
    
    print("=== DEPLOIEMENT AVEC GIT ===")
    print()
    
    commands = [
        # Initialise Git
        "git init",
        "git add .",
        'git commit -m "Initial commit"',
        
        # Ajoute le remote (remplace avec ton repo)
        'git remote add origin https://github.com/TON_USERNAME/smartchoice-ecommerce.git',
        'git branch -M main',
        'git push -u origin main'
    ]
    
    print("Commandes à exécuter:")
    print()
    for cmd in commands:
        print(f"   {cmd}")
    
    print()
    print("=== COMMANDE COMPLETE ===")
    print()
    print("git init && git add . && git commit -m 'Deploy' && git remote add origin https://github.com/TON_USERNAME/smartchoice-ecommerce.git && git push -u origin main")
    print()
    print("Ensuite va sur Render/Railway et connecte ton repo GitHub !")

def create_deploy_script():
    """Crée un script de déploiement automatique"""
    
    script_content = '''@echo off
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
'''
    
    with open('deploy.bat', 'w') as f:
        f.write(script_content)
    
    print("✓ Script 'deploy.bat' créé !")
    print("✓ Double-clique dessus pour déployer automatiquement")

if __name__ == "__main__":
    deploy_with_git()
    create_deploy_script()
