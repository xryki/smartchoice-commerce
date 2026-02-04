# Déploiement local avec ngrok (pour tester immédiatement)

import subprocess
import sys
import time

def deploy_with_ngrok():
    """Déploie localement avec ngrok pour accès externe"""
    
    print("=== DEPLOIEMENT LOCAL AVEC NGROK ===")
    print()
    
    print("1. Installe ngrok:")
    print("   pip install pyngrok")
    print()
    
    print("2. Lance le serveur Flask:")
    print("   python app_clean.py")
    print()
    
    print("3. Dans un autre terminal, lance ngrok:")
    print("   ngrok http 5000")
    print()
    
    print("4. ngrok te donnera une URL publique comme:")
    print("   https://abc123.ngrok.io")
    print()
    
    print("5. Partage cette URL - tout le monde peut y accéder!")
    print()
    
    # Test si pyngrok est installé
    try:
        from pyngrok import ngrok
        
        print("Lancement de ngrok...")
        public_url = ngrok.connect(5000)
        print(f"URL PUBLIQUE: {public_url}")
        print("Ton site est accessible en ligne!")
        print("Partage cette URL avec qui tu veux!")
        
        # Garde ngrok actif
        input("Appuie sur Enter pour arrêter...")
        ngrok.disconnect(public_url)
        
    except ImportError:
        print("Installe d'abord ngrok: pip install pyngrok")
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    deploy_with_ngrok()
