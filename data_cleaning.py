import re
import numpy as np

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\b\w{1,2}\b', '', text)  # Supprimer les mots de 1 ou 2 caractères
    text = re.sub(r'\s+', ' ', text)  # Remplacer les espaces multiples par un seul espace
    text = re.sub(r'[^\w\s]', '', text)  # Supprimer la ponctuation
    return text



# Fonctions pour les transformations
def get_text(df):
    return df['text_cleaned']

def get_text_length(df):
    return np.array(df['text_length']).reshape(-1, 1)

def get_num_words(df):
    return np.array(df['num_words']).reshape(-1, 1)

def get_num_sentences(df):
    return np.array(df['num_sentences']).reshape(-1, 1)

def get_num_links(df):
    return np.array(df['num_links']).reshape(-1, 1)

def get_num_emails(df):
    return np.array(df['num_emails']).reshape(-1, 1)

def get_num_special_chars(df):
    return np.array(df['num_special_chars']).reshape(-1, 1)

def get_uppercase_ratio(df):
    return np.array(df['uppercase_ratio']).reshape(-1, 1)
