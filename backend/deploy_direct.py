# Déploiement DIRECT avec Render CLI

import subprocess
import sys
import os

def deploy_render_cli():
    """Déploie directement avec Render CLI dans le terminal"""
    
    print("=== DEPLOIEMENT DIRECT AVEC RENDER CLI ===")
    print()
    
    print("1. Installation de Render CLI:")
    print("   npm install -g @render/cli")
    print()
    
    print("2. Connexion à Render:")
    print("   render login")
    print("   (ça va ouvrir ton navigateur pour te connecter)")
    print()
    
    print("3. Déploie ton projet:")
    print("   render deploy")
    print()
    
    print("4. Render va:")
    print("   - Détecter automatiquement ton app Python")
    print("   - Installer les dépendances")
    print("   - Lancer ton application")
    print("   - Te donner l'URL publique")
    print()
    
    print("=== COMMANDE COMPLETE A EXECUTER ===")
    print()
    print("npm install -g @render/cli && render login && render deploy")
    print()
    print("Une seule commande et ton site est en ligne !")
    
    # Vérifie si on peut exécuter
    try:
        print("\n=== TEST DE L'ENVIRONNEMENT ===")
        
        # Vérifie si npm est installé
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ npm version: {result.stdout.strip()}")
            print("✓ Tu peux utiliser Render CLI !")
        else:
            print("❌ npm n'est pas installé")
            print("Installe Node.js depuis https://nodejs.org/")
            
    except FileNotFoundError:
        print("❌ npm n'est pas installé")
        print("Installe Node.js depuis https://nodejs.org/")

def deploy_heroku_cli():
    """Alternative: Déploiement avec Heroku CLI"""
    
    print("\n=== ALTERNATIVE: HEROKU CLI ===")
    print()
    print("1. Installation Heroku CLI:")
    print("   npm install -g heroku")
    print()
    print("2. Connexion:")
    print("   heroku login")
    print()
    print("3. Crée l'app:")
    print("   heroku create smartchoice-ecommerce")
    print()
    print("4. Déploie:")
    print("   git add .")
    print("   git commit -m 'Deploy'")
    print("   git push heroku main")
    print()
    print("TON URL: https://smartchoice-ecommerce.herokuapp.com")

if __name__ == "__main__":
    deploy_render_cli()
    deploy_heroku_cli()
