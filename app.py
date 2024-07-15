# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template
import pickle
import logging
import sqlite3
from data_cleaning import clean_text, get_text, get_text_length, get_num_words, get_num_sentences, get_num_links, get_num_emails, get_num_special_chars, get_uppercase_ratio
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


app = Flask(__name__)

# Configurer les logs
logging.basicConfig(level=logging.DEBUG)

# Charger le pipeline (modèle + vectoriseur)
with open('spam_classifier_pipeline.pkl', 'rb') as f:
    pipeline = pickle.load(f)

# Initialiser la base de données
def init_db():
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS predictions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  text TEXT, 
                  prediction TEXT, 
                  actual TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True) if request.is_json else request.form
        text = data.get('text')
        cleaned_text = clean_text(text)
        logging.debug(f"Texte reçu: {text}")
        logging.debug(f"Texte nettoyé: {cleaned_text}")
        
        # Reformater le texte nettoyé en un tableau 2D
        text_array = np.array([cleaned_text])
        
        
        # Faire la prédiction en utilisant le pipeline complet
        prediction = pipeline.predict(text_array)[0]
        logging.debug(f"Prédiction brute: {prediction}")
        logging.debug(f"Type de prédiction: {type(prediction)}")

        # Si la prédiction est un tableau numpy, prenez la première valeur
        if isinstance(prediction, np.ndarray):
            prediction = prediction.item()

        logging.debug(f"Prédiction après conversion: {prediction}")
        
        # Obtenez la classe prédite
        prediction_label = str(prediction)
        logging.debug(f"Prédiction finale: {prediction_label}")
        
        # Vérifiez si le texte existe déjà dans la base de données
        conn = sqlite3.connect('predictions.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM predictions WHERE text = ?", (text,))
        result = c.fetchone()
        
        if result[0] == 0:
            # Enregistrer la prédiction dans la base de données
            c.execute("INSERT INTO predictions (text, prediction) VALUES (?, ?)", (text, prediction_label))
            conn.commit()
            logging.debug(f"Texte inséré dans la base de données: {text}")
        else:
            logging.debug(f"Le texte existe déjà dans la base de données: {text}")

        conn.close()
        
        return jsonify({'prediction': prediction_label})
    except Exception as e:
        logging.error(f"Erreur: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
def admin():
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    c.execute("SELECT id, text, prediction, actual FROM predictions WHERE actual IS NULL")
    rows = c.fetchall()
    conn.close()
    return render_template('admin.html', rows=rows)

@app.route('/update_prediction', methods=['POST'])
def update_prediction():
    try:
        data = request.form
        logging.debug(f"Data reçue: {data}")
        prediction_id = data.get('id')
        actual = data.get('actual')
        
        # Vérifiez que les champs ne sont pas None
        if not prediction_id or not actual:
            raise ValueError("Les champs 'id' et 'actual' sont requis.")
        
        # Assurez-vous que 'actual' est en minuscule
        actual = actual.lower()

        logging.debug(f"ID: {prediction_id}, Actual: {actual}")
        
        conn = sqlite3.connect('predictions.db')
        c = conn.cursor()
        c.execute("UPDATE predictions SET actual = ? WHERE id = ?", (actual, prediction_id))
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        logging.error(f"Erreur: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/view_predictions', methods=['GET'])
def view_predictions():
    try:
        conn = sqlite3.connect('predictions.db')
        c = conn.cursor()
        c.execute("SELECT * FROM predictions")
        rows = c.fetchall()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Fonction de réentraînement du modèle
def retrain_model():
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    query = """
    SELECT text, COALESCE(actual, prediction) as label FROM predictions
    """
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    texts = [clean_text(row[0]) for row in rows if row[0] and row[1]]
    labels = [row[1] for row in rows if row[0] and row[1]]
    
    if not texts or not labels:
        raise ValueError("No data available for retraining.")
    
    # Encoder les labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(labels)
    
    # Créer un pipeline pour vectoriser les textes et entraîner le modèle
    pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', LogisticRegression())
    ])
    
    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(texts, y, test_size=0.2, random_state=42)
    
    # Entraîner le modèle
    pipeline.fit(X_train, y_train)
    
    # Sauvegarder le pipeline entier (modèle + vectoriseur)
    with open('spam_classifier_pipeline.pkl', 'wb') as f:
        pickle.dump(pipeline, f)

    # Afficher les performances du modèle
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
