# Projet LLM

## Structure du projet
- **data** : Contient les fichiers CSV des cours et étudiants.
- **local** : Code source du projet.
  - `agent.py` : Gestion des agents.
  - `app.py` : Application principale.
  - `load.py` : Chargement des données.

## Installation
1. Clonez le projet :
   ```bash
   git clone <url_du_dépôt>
   cd <nom_du_dossier>

2. Créez un environnement virtuel et activez-le :
    ```bash
    python -m venv env
    source env/bin/activate  # Linux/Mac
    env\Scripts\activate     # Windows

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt

4. Créer le dossier pour le stockage des vecteurs :
    Créer à la racine le dossier **embeddings/** s'il existe pas !

## Utilisation

Lancez le fichier app.py :
    
    python local-file/app.py



