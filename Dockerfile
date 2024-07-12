# Utilisez une image de base officielle de Python
FROM python:3.10-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requirements et app
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY spam_classifier_pipeline.pkl spam_classifier_pipeline.pkl
#COPY spam_classifier.pkl spam_classifier.pkl
#COPY tfidf_vectorizer.pkl tfidf_vectorizer.pkl
COPY templates/ templates/
COPY static/ static/

# Installer les dépendances
RUN pip install -r requirements.txt

# Exposer le port sur lequel l'application va fonctionner
EXPOSE 5000

# Définir la commande pour exécuter l'application
CMD ["python", "app.py"]
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]