# Guide d'installation et d'utilisation du Système RAG Télécom

## 📋 Prérequis

1. **Python 3.10 ou 3.11** installé
2. **Ollama** installé et démarré
3. **Modèle Mistral** téléchargé via Ollama

## 🚀 Installation

### Étape 1 : Créer l'environnement virtuel

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate

# Activer l'environnement (Linux/Mac)
source venv/bin/activate
```

### Étape 2 : Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Étape 3 : Configurer les variables d'environnement

```bash
# Copier le fichier exemple
copy .env.example .env

# Éditer .env si nécessaire (les valeurs par défaut fonctionnent)
```

### Étape 4 : Installer et démarrer Ollama

```bash
# Télécharger Ollama depuis https://ollama.com/download

# Démarrer Ollama
ollama serve

# Dans un autre terminal, télécharger Mistral
ollama pull mistral
```

### Étape 5 : Ajouter des documents

Ajoutez vos documents PDF, DOCX ou TXT dans le dossier `data/raw/`

**Note :** Le dossier `data/raw/` est dans `.gitignore` pour la sécurité.
Créez-le manuellement et ajoutez vos documents.

### Étape 6 : Construire la base vectorielle

```bash
python src/build_vectorstore.py
```

### Étape 7 : Lancer l'application Streamlit

```bash
streamlit run app/streamlit_app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

## 📁 Structure du projet

```
telecom_project/
├── app/
│   └── streamlit_app.py          # Interface Streamlit
├── src/
│   ├── __init__.py
│   ├── config.py                 # Configuration
│   ├── data_loader.py            # Chargement documents
│   ├── embeddings.py             # Génération embeddings
│   ├── vectorstore.py            # Gestion FAISS
│   ├── llm.py                    # Gestion LLM Ollama
│   ├── rag_pipeline.py           # Pipeline RAG complet
│   └── build_vectorstore.py      # Script d'indexation
├── data/
│   └── raw/                      # Vos documents (à créer)
├── vectorstore/                  # Base vectorielle (généré)
├── requirements.txt              # Dépendances Python
├── .env.example                  # Exemple de configuration
└── README.md                     # Documentation complète
```

## 🧪 Tester le système

### Test rapide du pipeline

```bash
python src/rag_pipeline.py
```

### Poser une question via Python

```python
from src.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
result = pipeline.query("Quelles sont les offres disponibles ?")
print(result['answer'])
```

## 🎨 Personnalisation

### Modifier les couleurs (charte YAS)

Éditez `src/config.py` :

```python
COLORS = {
    "primary": "#6B2D8F",      # Violet YAS
    "secondary": "#00D9A3",    # Vert accent
    "background": "#F5F5F5",   # Gris clair
    "text": "#2C2C2C"          # Gris foncé
}
```

### Ajuster les paramètres RAG

Éditez `.env` :

```
CHUNK_SIZE=800              # Taille des chunks
CHUNK_OVERLAP=200           # Chevauchement
TOP_K_RETRIEVAL=5           # Nombre de sources
```

## ❓ Dépannage

### Erreur : "Ollama not connected"

```bash
# Vérifier qu'Ollama est démarré
ollama serve

# Vérifier que Mistral est téléchargé
ollama list
```

### Erreur : "Base vectorielle non trouvée"

```bash
# Reconstruire la base vectorielle
python src/build_vectorstore.py
```

### Erreur lors de l'installation des dépendances

```bash
# Mettre à jour pip
pip install --upgrade pip

# Réinstaller
pip install -r requirements.txt --no-cache-dir
```

## 📞 Support

Pour toute question sur le projet académique, consultez la documentation complète dans `README.md`.
