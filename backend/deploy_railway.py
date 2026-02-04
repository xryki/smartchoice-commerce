# Déploiement sur Railway (le plus rapide)

import sys
import os

def deploy_railway():
    """Instructions pour déployer sur Railway"""
    
    print("=== DEPLOIEMENT RAILWAY ===")
    print()
    
    print("1. Crée un compte sur https://railway.app/")
    print("2. Connecte ton compte GitHub")
    print("3. Crée un nouveau repo GitHub")
    print("4. Upload tous tes fichiers sur GitHub")
    print()
    
    print("5. Sur Railway: 'New Project' -> 'Deploy from GitHub repo'")
    print("6. Sélectionne ton repo")
    print("7. Railway détecte automatiquement Python")
    print()
    
    print("8. Ajoute un fichier railway.json:")
    print("""
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app_clean.py",
    "healthcheckPath": "/"
  }
}
""")
    
    print("9. Ajoute les variables d'environnement:")
    print("   - PORT: 5000")
    print("   - PYTHONPATH: /app")
    print()
    
    print("10. Clique sur 'Deploy Now'")
    print()
    print("TON SITE SERA ACCESSIBLE: https://ton-projet.railway.app")

if __name__ == "__main__":
    deploy_railway()
