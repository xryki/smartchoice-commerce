# Déploiement sur Render (plus moderne)

import sys
import os

def deploy_render():
    """Instructions pour déployer sur Render"""
    
    print("=== DEPLOIEMENT RENDER ===")
    print()
    
    print("1. Crée un compte sur https://render.com/")
    print("2. Connecte ton compte GitHub")
    print("3. Crée un nouveau repo GitHub avec ton projet")
    print("4. Sur Render: 'New +' -> 'Web Service'")
    print("5. Connecte ton repo GitHub")
    print()
    
    print("6. Configure le service:")
    print("   - Name: smartchoice-ecommerce")
    print("   - Runtime: Python 3")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: python app_clean.py")
    print("   - Instance Type: Free")
    print()
    
    print("7. Ajoute ces variables d'environnement:")
    print("""
PYTHONPATH=/app
FLASK_APP=app_clean.py
FLASK_ENV=production
""")
    
    print("8. Crée le fichier render.yaml:")
    print("""
services:
  - type: web
    name: smartchoice
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app_clean.py
    envVars:
      - key: PYTHONPATH
        value: /app
""")
    
    print("9. Push ton code sur GitHub")
    print("10. Render déploie automatiquement")
    print()
    print("TON SITE SERA ACCESSIBLE: https://smartchoice-ecommerce.onrender.com")

if __name__ == "__main__":
    deploy_render()
