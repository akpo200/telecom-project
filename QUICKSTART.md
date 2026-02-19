# 🎯 GUIDE DE DÉMARRAGE RAPIDE


### 📦 Code source (`src/`)
- ✅ `config.py` - Configuration centralisée
- ✅ `data_loader.py` - Chargement et découpage des documents
- ✅ `embeddings.py` - Génération des embeddings
- ✅ `vectorstore.py` - Gestion de la base vectorielle FAISS
- ✅ `llm.py` - Gestion du LLM Ollama/Mistral
- ✅ `rag_pipeline.py` - Pipeline RAG complet
- ✅ `build_vectorstore.py` - Script d'indexation

### 🎨 Interface (`app/`)
- ✅ `streamlit_app.py` - Interface web avec charte YAS

### ⚙️ Configuration
- ✅ `requirements.txt` - Dépendances Python
- ✅ `.env.example` - Configuration exemple
- ✅ `.gitignore` - Fichiers à ignorer
- ✅ `INSTALLATION.md` - Guide d'installation détaillé

## 🚀 PROCHAINES ÉTAPES

### 1. Installer Ollama et Mistral

```powershell
# Télécharger Ollama depuis https://ollama.com/download
# Installer et démarrer Ollama

# Télécharger Mistral
ollama pull mistral
```

### 2. Créer l'environnement virtuel

```powershell
# Créer l'environnement
python -m venv venv

# Activer
.\venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configurer l'environnement

```powershell
# Copier la configuration
copy .env.example .env
```

### 4. Ajouter vos documents

**IMPORTANT** : Le dossier `data/raw/` est dans `.gitignore` pour la sécurité.

Créez-le et ajoutez vos documents :

```powershell
# Les sous-dossiers ont été créés automatiquement
# Ajoutez vos documents PDF, DOCX ou TXT dans :
# - data/raw/offres_commerciales/
# - data/raw/procedures_techniques/
# - data/raw/conditions_generales/
```

### 5. Construire la base vectorielle

```powershell
python src\build_vectorstore.py
```

### 6. Lancer l'application

```powershell
streamlit run app\streamlit_app.py
```

## 📚 Documentation

- **README.md** : Documentation académique complète (PARTIES 1 & 2)
- **INSTALLATION.md** : Guide d'installation détaillé
- **Code source** : Tous les fichiers sont commentés en français

## 🎨 Charte graphique YAS

L'interface utilise les couleurs de YAS :
- Violet principal : `#6B2D8F`
- Vert accent : `#00D9A3`
- Fond : `#F5F5F5`
- Texte : `#2C2C2C`

## 💡 Besoin d'aide ?

Consultez `INSTALLATION.md` pour le guide complet et le dépannage.

---

**✅ PROJET PRÊT À ÊTRE UTILISÉ !**
