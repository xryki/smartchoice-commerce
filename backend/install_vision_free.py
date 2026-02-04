# Installation des dépendances GRATUITES pour la vision

import subprocess
import sys

def install_free_vision():
    """Installe toutes les dépendances gratuites pour la reconnaissance d'objets"""
    
    packages = [
        "torch",  # PyTorch (gratuit)
        "transformers",  # Hugging Face (gratuit)
        "pillow",  # Traitement d'images
        "opencv-python",  # OpenCV (gratuit)
        "numpy",  # Calcul numérique
        "requests",  # Pour les requêtes API
    ]
    
    print("Installation des packages GRATUITS pour la vision...")
    print("Cela peut prendre quelques minutes...")
    
    for package in packages:
        try:
            print(f"Installation de {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installe avec succes!")
        except Exception as e:
            print(f"Erreur installation {package}: {e}")
    
    print("\nInstallation terminee!")
    print("Maintenant tu peux utiliser vision_free.py gratuitement!")

if __name__ == "__main__":
    install_free_vision()
