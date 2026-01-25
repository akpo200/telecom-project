"""
Module de configuration du système RAG
Charge les variables d'environnement et définit les paramètres globaux
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Chemins de base
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
VECTORSTORE_DIR = BASE_DIR / "vectorstore" / "faiss_index"

# Configuration Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

# Configuration Embeddings
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL", 
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# Configuration RAG
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "5"))

# Configuration API externes (optionnel)
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", None)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

# Créer les dossiers s'ils n'existent pas
DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

# Couleurs YAS pour l'interface
COLORS = {
    "primary": "#6B2D8F",      # Violet YAS
    "secondary": "#00D9A3",    # Vert accent
    "background": "#F5F5F5",   # Gris clair
    "text": "#2C2C2C"          # Gris foncé
}

print(f"✅ Configuration chargée depuis {BASE_DIR}")
print(f"📁 Dossier de données : {DATA_DIR}")
print(f"🗄️ Dossier vectorstore : {VECTORSTORE_DIR}")
