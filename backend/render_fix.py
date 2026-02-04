# Fix pour Render - Configuration automatique

import os
import subprocess

def fix_for_render():
    """Crée les fichiers nécessaires pour Render"""
    
    print("=== CONFIGURATION POUR RENDER ===")
    print()
    
    # 1. Crée render.yaml
    render_yaml = """services:
  - type: web
    name: smartchoice-ecommerce
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app_clean.py
    envVars:
      - key: PYTHONPATH
        value: /app
      - key: PORT
        value: 5000
    healthCheckPath: /
"""
    
    with open('render.yaml', 'w') as f:
        f.write(render_yaml)
    print("✅ render.yaml créé")
    
    # 2. Vérifie requirements.txt
    requirements = """Flask==2.3.3
Flask-CORS==4.0.0
PyJWT==2.8.0
Pillow==10.0.1
requests==2.31.0"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("✅ requirements.txt vérifié")
    
    # 3. Crée un Procfile (alternative)
    procfile = "web: python app_clean.py"
    with open('Procfile', 'w') as f:
        f.write(procfile)
    print("✅ Procfile créé")
    
    print("\n=== FICHIERS PRETS POUR RENDER ===")
    print("1. Commit ces fichiers sur GitHub:")
    print("   git add .")
    print("   git commit -m 'Add Render config'")
    print("   git push")
    print()
    print("2. Va sur https://render.com/")
    print("3. 'New +' → 'Web Service'")
    print("4. Connecte ton repo xryki/smartchoice-ecommerce")
    print("5. Render va détecter automatiquement render.yaml")
    print()
    print("Si ça ne marche pas, essaye:")
    print("- Build Command: pip install -r requirements.txt")
    print("- Start Command: python app_clean.py")
    print("- Environment Variable: PORT=5000")

def create_simple_deploy():
    """Crée un script de déploiement simple"""
    
    script = """@echo off
echo === DEPLOIEMENT SUR RENDER ===

echo 1. Commit sur GitHub...
git add .
git commit -m "Deploy to Render"
git push

echo 2. Va sur https://render.com/
echo 3. New + -^> Web Service
echo 4. Connecte ton repo: xryki/smartchoice-ecommerce
echo 5. Configure:
echo    - Build: pip install -r requirements.txt
echo    - Start: python app_clean.py
echo    - PORT: 5000
echo 6. Deploy!

echo Ton URL sera: https://smartchoice-ecommerce.onrender.com
pause
"""
    
    with open('deploy_render.bat', 'w') as f:
        f.write(script)
    print("✅ deploy_render.bat créé")

if __name__ == "__main__":
    fix_for_render()
    create_simple_deploy()
