import pyodbc
import requests
import json

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
    
    # 1. Connexion à ton SQL Server Local (Authentification Windows complète)
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost;"
        "Database=master;" # Remplace par le nom de ta base si nécessaire
        "Trusted_Connection=yes;"
    )
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print("⚡ Connexion à SQL Server réussie !")
        
        # 2. Sélectionner les boissons qui n'ont pas encore de vecteur
        cursor.execute("SELECT BoissonID, Nom, Description FROM dbo.BoissonsBienEtre WHERE VectorText IS NULL")
        lignes = cursor.fetchall()
        
        if not lignes:
            print("✅ Toutes les boissons sont déjà vectorisées.")
            return

        print(f"🔄 {len(lignes)} boisson(s) à vectoriser...")
        
        # 3. Boucle de mise à jour
        for ligne in lignes:
            boisson_id, nom, description = ligne
            texte_a_vectoriser = f"{nom} | {description}"
            
            # Génération du vecteur
            vecteur = get_embedding(texte_a_vectoriser)
            
            # Transformation de la liste de floats en texte JSON pour le stocker dans le NVARCHAR(MAX)
            vecteur_json = json.dumps(vecteur)
            
            # Enregistrement dans le SQL
            cursor.execute(
                "UPDATE dbo.BoissonsBienEtre SET VectorText = ? WHERE BoissonID = ?",
                (vecteur_json, boisson_id)
            )
            print(f"✨ Vecteur enregistré pour : {nom}")
            
        # Validation des changements
        conn.commit()
        print("💾 Base de données mise à jour et sauvegardée avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    connecter_et_vectoriser()