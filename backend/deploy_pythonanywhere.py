# Déploiement sur PythonAnywhere

import sys
import os

def deploy_pythonanywhere():
    """Instructions pour déployer sur PythonAnywhere"""
    
    print("=== DEPLOIEMENT PYTHONANYWHERE ===")
    print()
    
    print("1. Crée un compte gratuit sur https://www.pythonanywhere.com/")
    print("2. Va vers 'Web' -> 'Add a new web app'")
    print("3. Choisis 'Flask' et Python 3.10+")
    print("4. Upload tes fichiers:")
    print("   - app_clean.py")
    print("   - models_fixed.py") 
    print("   - vision_simple.py")
    print("   - products_part1.py")
    print("   - products_part2_clean.py")
    print("   - requirements.txt")
    print()
    
    print("5. Crée requirements.txt avec:")
    print("""
Flask==2.3.3
Flask-CORS==4.0.0
PyJWT==2.8.0
Pillow==10.0.1
requests==2.31.0
""")
    
    print("6. Dans la console PythonAnywhere:")
    print("   pip install -r requirements.txt")
    print("   python models_fixed.py  # Pour initialiser la BDD")
    print()
    
    print("7. Configure le WSGI:")
    print("""
import sys
sys.path.append('/home/tonusername/tonproject')
from app_clean import app as application
""")
    
    print("8. Redémarre le serveur web")
    print()
    print("TON SITE SERA ACCESSIBLE: https://tonusername.pythonanywhere.com")

if __name__ == "__main__":
    deploy_pythonanywhere()
