# RechercherBoissonIdeal
Moteur de recherche RAG 100% local appliqué aux boissons. 
Une architecture 3-Tier associant SQL Server, Python et Streamlit. L'application utilise Ollama (nomic-embed-text et llama3) pour comprendre l'intention de l'utilisateur et générer des réponses adaptées sans aucune API cloud payante.

# Inspiration de ce projet
J'ai suivie chez microsoft un mini cours intitulé Data Pro - Implémenter des capacités d’IA dans les solutions SQL Server lors du AI Skills Fest, malheureusement, je n'ai pas pu réalisé pour l'instant l'exercice que je vous laisse dans la branche ExerciceMicrosoft mais qui m'a inspiré à réalisé celui ci. Un projet qui n'a donc pas besoin d'un abonnement Azure.

# 🍵 Moteur de Recherche Sémantique & RAG Local — Boissons Bien-Être

Ce projet présente un système de **RAG (*Retrieval-Augmented Generation*)** local et natif** appliqué à un catalogue de boissons holistiques et bien-être. Contrairement à une recherche par mots-clés classique, ce moteur de recherche utilise l'**intelligence artificielle sémantique** pour comprendre l'intention sous-jacente de l'utilisateur (par exemple, associer une demande sur "le stress du soir" à une infusion relaxante, même si le mot "stress" n'est pas présent dans la fiche produit).

L'intégralité du projet tourne **à 100% en local**, garantissant la confidentialité des données et la gratuité d'exécution, sans dépendre d'API cloud payantes.

---

## Architecture du Projet (3-Tier)

Le projet est structuré selon une architecture standard à 3 couches :
1. **Base de données (Stockage) :** SQL Server stocke le catalogue de produits et leurs empreintes mathématiques (vecteurs).
2. **Backend & IA (Traitement) :** Python fait le lien entre la base de données, le calcul de similarité vectorielle (NumPy) et les modèles d'IA locaux (Ollama).
3. **Interface Utilisateur (Présentation) :** Une application web moderne et épurée développée avec Streamlit.

---

## Outils Utilisées

* **Base de données :** SQL Server (Transact-SQL)
* **Orchestration & Backend :** Python 3.13+
* **Modèles d'IA (via Ollama) :**
    * nomic-embed-text : Pour la génération des embeddings (vecteurs de 768 dimensions).
    * llama3 : Pour la génération de réponses textuelles fluides et chaleureuses.
* **Bibliothèques Python clés :** 'streamlit', 'pyodbc', 'numpy', 'requests'

---

## Structure des Fichiers

* cacao_rag_full.sql : Script SQL de création de la table 'dbo.BoissonsBienEtre' et d'insertion du jeu de données initial.
* initialiser_sql.py : Script administrateur Python. Il récupère les produits du SQL sans signature numérique, appelle le modèle d'embedding d'Ollama, et sauvegarde le résultat au format JSON directement dans la base SQL.
* app.py : L'application principale Streamlit qui gère la barre de recherche utilisateur, calcule la similarité cosinus et affiche la réponse du sommelier IA.

---

## Installation et Lancement

### 1. Prérequis
* Avoir installé [Ollama](https://ollama.com/) et récupéré les modèles requis à executer dans votre cmd :
    ```
    ollama run nomic-embed-text
    ollama run llama3
    ```
* Un serveur **SQL Server** local actif.

### 2. Configuration de la Base de Données
Exécutez le script contenu dans 'cacao_rag_full.sql' sur votre instance SQL Server pour initialiser la table.

### 3. Installation des dépendances Python
Installez les packages nécessaires à l'aide de 'pip' :
```
pip install streamlit requests numpy pyod
```
