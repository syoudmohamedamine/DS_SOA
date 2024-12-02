# Utilisation d'une image de base (Python)
FROM python:3.11

# Répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copier les fichiers requis et installer les dépendances
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Assure-toi que gunicorn est installé
RUN pip install gunicorn

# Copier le reste des fichiers de l'application
COPY . /app

# Commande pour lancer gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myapp.wsgi:application"]
