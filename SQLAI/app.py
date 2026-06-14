import streamlit as st
import requests
import json
import numpy as np
import sqlite3

st.set_page_config(page_title="Barre de Recherche IA - Boissons", page_icon="🍵")
st.title("🤖 Moteur de recherche sémantique (SQL + Ollama)")

#FONCTIONS IA & DATA

def charger_catalogue_depuis_sqlite():
    '''
    None --> list
    Se connecte à la base SQL pour charger les boissons et convertir le texte JSON en vrais vecteurs utilisables par NumPy.
    '''
    catalogue = []
    try:
        conn = sqlite3.connect("boissons.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Nom, Type, Description, VectorText FROM BoissonsBienEtre") #récupration des données
        lignes = cursor.fetchall()

        for row in lignes:
            # Si le produit n'a pas de vecteur dans la base, on passe
            if row[3] is None:
                continue
                
            catalogue.append({
                "Nom": row[0],
                "Type": row[1],
                "Description": row[2],
                "Vecteur": json.loads(row[3]) # On retransforme le texte JSON en liste de floats
            })
        conn.close()
    except Exception as e:
        st.error(f"Erreur de connexion SQL : {e}")
    return catalogue


def get_embedding(texte):
    '''
    str --> list
    Envoie un texte au modèle local 'nomic-embed-text' d'Ollama et 
    récupère sa signature vectorielle (une liste de nombres flottants).
    '''
    url = "http://localhost:11434/api/embeddings"
    payload = {"model": "nomic-embed-text", "prompt": texte}
    response = requests.post(url, json=payload)
    return response.json()["embedding"]


def calcul_similarite(v1, v2):
    '''
    list x list --> float 
    Calcule la similarité cosinus entre deux vecteurs. 
    Plus le score est proche de 1, plus les textes ont un sens similaire.
    '''
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def generer_reponse_ia(question, contexte_boisson):
    '''
    str x dict --> str
    Prend la question de l'utilisateur et le dictionnaire de la boisson trouvée, 
    puis demande à 'llama3' de rédiger une réponse fluide et personnalisée.
    '''
    url = "http://localhost:11434/api/generate"
    prompt = f"""
    Tu es un sommelier expert en boissons bien-être. 
    En utilisant UNIQUEMENT la boisson suivante, réponds à la question de l'utilisateur de manière chaleureuse et courte.
    
    Boisson recommandée : {contexte_boisson['Nom']} ({contexte_boisson['Type']}) - {contexte_boisson['Description']}
    
    Question de l'utilisateur : {question}
    """
    payload = {"model": "llama3", "prompt": prompt, "stream": False}
    response = requests.post(url, json=payload)
    return response.json()["response"]


#CHARGEMENT DU CATALOGUE
#L'application lit directement la base de données au lieu d'une liste figée !
BASE_BOISSONS = charger_catalogue_depuis_sqlite()



#INTERFACE GRAPHISQUE
recherche = st.text_input("Que recherchez-vous ?", placeholder="Ex: Une boisson pour calmer mon anxiété le soir...")

if recherche:
    if not BASE_BOISSONS:
        st.warning("⚠️ Le catalogue est vide. Pense à lancer le script 'initialiser_sql.py' pour synchroniser tes données SQL !")
    else:
        with st.spinner("Recherche sémantique dans la base SQL... 🧠"):
            vecteur_recherche = get_embedding(recherche)
            
            meilleure_boisson = None
            meilleur_score = -1.0
            
            for b in BASE_BOISSONS:
                score = calcul_similarite(vecteur_recherche, b["Vecteur"])
                if score > meilleur_score:
                    meilleur_score = score
                    meilleure_boisson = b
            
            if meilleure_boisson:
                reponse_finale = generer_reponse_ia(recherche, meilleure_boisson)
                st.success(f"Produit extrait de SQL : **{meilleure_boisson['Nom']}** (Score : {meilleur_score:.2f})")
                st.chat_message("assistant").write(reponse_finale)
