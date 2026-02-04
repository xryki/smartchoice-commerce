FROM python:3.9-slim

WORKDIR /app

# Copie les fichiers nécessaires
COPY requirements.txt .
COPY app_render.py .
COPY models_fixed.py .
COPY vision_simple.py .
COPY products_part1.py .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Initialise la base de données
RUN python models_fixed.py

# Expose le port
EXPOSE 5000

# Commande de démarrage
CMD ["python", "app_render.py"]
