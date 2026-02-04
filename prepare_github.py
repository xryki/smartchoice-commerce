# Script pour préparer les fichiers GitHub

import os
import shutil

def prepare_github_files():
    """Crée un dossier avec seulement les fichiers nécessaires pour GitHub"""
    
    print("Préparation des fichiers pour GitHub...")
    
    # Crée le dossier de déploiement
    deploy_folder = "github_deploy"
    if os.path.exists(deploy_folder):
        shutil.rmtree(deploy_folder)
    
    os.makedirs(deploy_folder)
    
    # Fichiers à copier
    files_to_copy = [
        "backend/app_clean.py",
        "backend/models_fixed.py", 
        "backend/vision_simple.py",
        "backend/requirements.txt",
        "backend/products_part1.py",
        "backend/products_part2_clean.py"
    ]
    
    # Copie les fichiers
    for file_path in files_to_copy:
        if os.path.exists(file_path):
            filename = os.path.basename(file_path)
            shutil.copy2(file_path, f"{deploy_folder}/{filename}")
            print(f"✓ Copié: {filename}")
        else:
            print(f"❌ Manquant: {file_path}")
    
    print(f"\n📁 Dossier '{deploy_folder}' créé avec les fichiers GitHub")
    print("💡 Glisse ce dossier sur GitHub !")
    
    # Affiche le contenu
    print(f"\nContenu du dossier {deploy_folder}:")
    for file in os.listdir(deploy_folder):
        size = os.path.getsize(f"{deploy_folder}/{file}")
        print(f"  - {file} ({size} bytes)")

if __name__ == "__main__":
    prepare_github_files()
