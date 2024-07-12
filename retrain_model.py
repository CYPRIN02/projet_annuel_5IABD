import sqlite3
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from data_cleaning import clean_text

def retrain_model():
    conn = sqlite3.connect('predictions.db')
    c = conn.cursor()
    c.execute("SELECT text, actual FROM predictions WHERE actual IS NOT NULL")
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
        ('classifier', LogisticRegression(solver='saga', max_iter=1000))
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


# import os
# import pickle
# import numpy as np
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from azure.storage.blob import BlobServiceClient
# from data_cleaning import clean_text

# def upload_model_to_blob(file_path, container_name, blob_name):
#     blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
#     blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
#     with open(file_path, "rb") as data:
#         blob_client.upload_blob(data, overwrite=True)

# def retrain_model():
#     conn = sqlite3.connect('predictions.db')
#     c = conn.cursor()
#     c.execute("SELECT text, actual FROM predictions WHERE actual IS NOT NULL")
#     rows = c.fetchall()
#     conn.close()

#     texts = [clean_text(row[0]) for row in rows if row[0] and row[1]]
#     labels = [row[1] for row in rows if row[0] and row[1]]
    
#     if not texts or not labels:
#         raise ValueError("No data available for retraining.")
    
#     label_encoder = LabelEncoder()
#     y = label_encoder.fit_transform(labels)
    
#     pipeline = Pipeline([
#         ('vectorizer', TfidfVectorizer()),
#         ('classifier', LogisticRegression(solver='saga', max_iter=1000))
#     ])
    
#     X_train, X_test, y_train, y_test = train_test_split(texts, y, test_size=0.2, random_state=42)
    
#     pipeline.fit(X_train, y_train)
    
#     model_path = 'spam_classifier_pipeline.pkl'
#     with open(model_path, 'wb') as f:
#         pickle.dump(pipeline, f)

#     upload_model_to_blob(model_path, 'your_container_name', 'spam_classifier_pipeline.pkl')

#     y_pred = pipeline.predict(X_test)
#     print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# if __name__ == '__main__':
#     retrain_model()
