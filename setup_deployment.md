# 🚀 Guide de Déploiement sur Streamlit Cloud

Pour héberger votre assistant YAS en ligne gratuitement, suivez ces étapes :

## 1. Préparer le Code sur GitHub
1.  Créez un nouveau dépôt (repository) sur votre compte GitHub.
2.  Poussez tout le code du projet sur ce dépôt.
    *   **Note** : Assurez-vous que le dossier `vectorstore/` est inclus si vous voulez que la base de connaissances soit disponible immédiatement.
    *   **Note** : Ne poussez **PAS** votre fichier `.env`. Utilisez les secrets de Streamlit (voir étape 2).

## 2. Configurer sur Streamlit Cloud
1.  Connectez-vous à [Streamlit Cloud](https://share.streamlit.io/).
2.  Cliquez sur **"New app"**.
3.  Sélectionnez votre dépôt, la branche (souvent `main`), et le chemin du fichier principal : `app/streamlit_app.py`.
4.  **IMPORTANT : Configurer les Secrets**
    *   Avant de lancer, allez dans **"Settings"** > **"Secrets"**.
    *   Copiez-collez le contenu de votre `.env` (ex: `GROQ_API_KEY=votre_cle`).
    *   Ajoutez également `PYTHONPATH=.` si nécessaire.

## 3. Dépendances
Le fichier `requirements.txt` à la racine sera automatiquement détecté par Streamlit pour installer les bibliothèques nécessaires.

## 4. Modèles d'Embeddings
Streamlit Cloud téléchargera automatiquement le modèle `sentence-transformers` lors du premier lancement. Cela peut prendre 1 à 2 minutes au premier démarrage.

---
**Besoin d'aide pour Git ?**
Si vous n'avez pas Git installé ou si vous ne savez pas comment pousser le code, je peux vous guider !
