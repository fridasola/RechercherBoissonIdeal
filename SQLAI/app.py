import streamlit as st
import requests
import json
import numpy as np # Pour calculer la similarité des vecteurs facilement

st.set_page_config(page_title="Barre de Recherche IA - Boissons", page_icon="🍵")
st.title("🤖 Moteur de recherche sémantique de Boissons")

# SIMULATION DE LA BASE DE DONNÉES (Pour l'exemple, transposable en SQL) avec une liste de dictionnaire
BASE_BOISSONS = [
    {
        "Nom": "Aurore Énergisante",
        "Type": "Cacao",
        "Description": "Alternative douce au café pour le matin. Stimule la concentration et réveille le corps en douceur pour un rituel sans stress.",
        "Vecteur": None
    },
    {
        "Nom": "Sérénité du Soir",
        "Type": "Infusion",
        "Description": "Boisson extra-fine aux notes florales et de vanille. Aide à relâcher l'anxiété et prépare à un sommeil profond.",
        "Vecteur": None
    },
    {
        "Nom": "Matcha Focus Ultra",
        "Type": "Thé Vert",
        "Description": "Thé vert moulu idéal pour une concentration prolongée l'après-midi sans le pic de stress du café. Riche en antioxydants.",
        "Vecteur": None
    }
]

#FONCTIONS IA VIA OLLAMA

# 1. Fonction pour générer un vecteur (Embedding)
@st.cache_data
def get_embedding(texte):
    ''' 
    str --> list
    Envoie un texte au modèle local 'nomic-embed-text' d'Ollama et récupère sa signature vectorielle 
    (une liste de nombres flottants).
    '''
    url = "http://localhost:11434/api/embeddings"
    payload = {"model": "nomic-embed-text", "prompt": texte}
    response = requests.post(url, json=payload)
    return response.json()["embedding"]

# Initialisation des vecteurs du catalogue (à faire une seule fois au lancement)
for b in BASE_BOISSONS:
    if b["Vecteur"] is None:
        # On vectorise le nom + la description pour donner du contexte à l'IA
        b["Vecteur"] = get_embedding(f"{b['Nom']} | {b['Description']}")

# 2. Calcul de similarité cosinus (Pour trouver le produit le plus proche)
def calcul_similarite(v1, v2):
    '''
    list x list --> float
    Calcule la similarité cosinus entre deux vecteurs. Plus le score est proche de 1, plus les textes ont un sens similaire.
    '''
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# 3. Génération de la réponse finale par l'IA
def generer_reponse_ia(question, contexte_boisson):
    '''
    str x dict --> str
    Prend la question de l'utilisateur et le dictionnaire de la boisson trouvée, puis demande à 'llama3' de rédiger une réponse 
    fluide et personnalisée.
    '''
    url = "http://localhost:11434/api/generate"
    prompt = f"""
    Tu es un sommelier expert en boissons bien-être. 
    En utilisant UNIQUEMENT la boisson suivante, réponds à la question de l'utilisateur de manière chaleureuse.
    
    Boisson recommandée : {contexte_boisson['Nom']} ({contexte_boisson['Type']}) - {contexte_boisson['Description']}
    
    Question de l'utilisateur : {question}
    """
    payload = {"model": "llama3", "prompt": prompt, "stream": False}
    response = requests.post(url, json=payload)
    return response.json()["response"]


# INTERFACE UTILISATEUR (La Barre de Recherche)

recherche = st.text_input("Que recherchez-vous ?", placeholder="Ex: Un truc pour me concentrer sans avoir le coeur qui bat à 100 à l'heure...")

if recherche:
    with st.spinner("Recherche sémantique en cours... 🧠"):
        # Étape 1 : On vectorise la demande de l'utilisateur
        vecteur_recherche = get_embedding(recherche)
        
        # Étape 2 : On cherche le produit le plus proche dans notre catalogue
        meilleure_boisson = None
        meilleur_score = -1
        
        for b in BASE_BOISSONS:
            score = calcul_similarite(vecteur_recherche, b["Vecteur"])
            if score > meilleur_score:
                meilleur_score = score
                meilleure_boisson = b
        
        # Étape C : On demande à l'IA de rédiger un texte sympa basé sur ce produit
        reponse_finale = generer_reponse_ia(recherche, meilleure_boisson)
        
        # Affichage
        st.success(f"Produit trouvé par ressemblance sémantique : **{meilleure_boisson['Nom']}** (Score: {meilleur_score:.2f})")
        st.chat_message("assistant").write(reponse_finale)