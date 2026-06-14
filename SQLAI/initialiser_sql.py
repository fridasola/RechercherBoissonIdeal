import sqlite3
import requests
import json
import os

def get_embedding(texte):
    '''
    str --> list
    Génère le vecteur d'un texte via Ollama
    '''
    url = "http://localhost:11434/api/embeddings"
    payload = {"model": "nomic-embed-text", "prompt": texte}
    response = requests.post(url, json=payload)
    return response.json()["embedding"]

def connecter_et_vectoriser():
    '''
    None --> None
    Se connecte à SQL Server, récupère les boissons sans vecteur,
    génère l'embedding et met à jour la base de données.
    '''
    try:
        base_existe = os.path.exists("boissons.db")
        # 1. Crée le fichier de base de données directement dans ton dossier !
        conn = sqlite3.connect("boissons.db")
        cursor = conn.cursor()
        
        if not base_existe:
            print("📜 Initialisation de la base avec le fichier SQL...")
            with open("cacao_rag_full.sql", "r", encoding="utf-8") as f:
                script_sql = f.read()
            
            # executescript permet de lancer tout le fichier d'un seul coup
            cursor.executescript(script_sql)
            conn.commit()
            print("✅ Table créée et boissons insérées !")

        # 2. Sélection des boissons à vectoriser (le reste ne change pas)
        cursor.execute("SELECT BoissonID, Nom, Description FROM BoissonsBienEtre WHERE VectorText IS NULL")
        lignes = cursor.fetchall()
        
        if not lignes:
            print("✅ Toutes les boissons sont déjà vectorisées.")
            
            return

        print(f"🔄 {len(lignes)} boisson(s) à vectoriser...")
        
        # 3. Boucle de mise à jour
        for ligne in lignes:
            boisson_id, nom, description = ligne
            vecteur = get_embedding(f"{nom} | {description}")
            cursor.execute("UPDATE BoissonsBienEtre SET VectorText = ? WHERE BoissonID = ?", (json.dumps(vecteur), boisson_id))
            print(f"✨ Vecteur enregistré pour : {nom}")
            
        conn.commit()
        print("💾 Base SQLite mise à jour avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    connecter_et_vectoriser()
