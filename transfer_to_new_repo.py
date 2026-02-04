# Script pour transférer vers le nouveau repo smart-choice_commerce

import subprocess
import os

def transfer_to_new_repo():
    """Transfère les fichiers vers smart-choice_commerce"""
    
    print("=== TRANSFERT VERS smart-choice_commerce ===")
    print()
    
    # Fichiers à copier
    files_to_transfer = [
        "backend/app_render.py",
        "backend/models_fixed.py", 
        "backend/vision_simple.py",
        "backend/requirements.txt",
        "backend/render.yaml",
        "backend/Procfile",
        "backend/products_part1.py"
    ]
    
    print("Fichiers à transférer:")
    for file in files_to_transfer:
        print(f"  ✓ {file}")
    
    print()
    print("=== COMMANDES À EXÉCUTER ===")
    print()
    print("1. Crée le nouveau repo sur GitHub: smart-choice_commerce")
    print("2. Clone le nouveau repo:")
    print("   git clone https://github.com/xryki/smart-choice_commerce.git")
    print("   cd smart-choice_commerce")
    print()
    print("3. Crée le dossier backend:")
    print("   mkdir backend")
    print()
    print("4. Copie les fichiers:")
    for file in files_to_transfer:
        print(f"   cp ../smart-choice/{file} {file}")
    
    print()
    print("5. Commit et push:")
    print("   git add .")
    print("   git commit -m 'Initial deploy'")
    print("   git push")
    print()
    print("6. Va sur Render et connecte smart-choice_commerce")

if __name__ == "__main__":
    transfer_to_new_repo()
