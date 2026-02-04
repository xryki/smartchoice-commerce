FROM python:3.9-slim

WORKDIR /app

# Copie d'abord les requirements pour optimiser le cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tous les fichiers du backend
COPY . .

# Initialise la base de données
RUN python models_fixed.py

# Expose le port
EXPOSE 5000

# Commande de démarrage
CMD ["python", "app_render.py"]
