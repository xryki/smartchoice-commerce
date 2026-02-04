# Nettoyage pour Railway - Supprime tous les fichiers Render

import subprocess
import os
import shutil

def clean_for_railway():
    """Supprime tous les fichiers Render et prépare pour Railway"""
    
    print("=== NETTOYAGE POUR RAILWAY ===")
    print()
    
    # Fichiers Render à supprimer
    render_files = [
        "backend/Dockerfile",
        "backend/render.yaml",
        "backend/Procfile"
    ]
    
    # Supprime les fichiers Render
    for file_path in render_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"❌ Supprimé: {file_path}")
        else:
            print(f"⚠️  Déjà absent: {file_path}")
    
    # Crée railway.json
    railway_config = """{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app_render.py",
    "healthcheckPath": "/"
  }
}"""
    
    with open('railway.json', 'w') as f:
        f.write(railway_config)
    print("✅ Créé: railway.json")
    
    # Vérifie les fichiers restants
    print("\n=== FICHIERS RESTANTS POUR RAILWAY ===")
    required_files = [
        "backend/app_render.py",
        "backend/models_fixed.py",
        "backend/vision_simple.py", 
        "backend/requirements.txt",
        "backend/products_part1.py",
        "railway.json"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ Manquant: {file_path}")
    
    print("\n=== PRÊT POUR RAILWAY ===")
    print("1. git add .")
    print("2. git commit -m 'Clean for Railway'")
    print("3. git push")
    print("4. Va sur https://railway.app/")
    print("5. New Project → Deploy from GitHub")
    print("6. Sélectionne smartchoice-ecommerce")
    print("7. Ajoute PORT=5000 en variable d'environnement")

if __name__ == "__main__":
    clean_for_railway()
