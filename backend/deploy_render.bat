@echo off
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
