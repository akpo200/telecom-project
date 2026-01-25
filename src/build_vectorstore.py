"""
Script pour construire la base vectorielle
À exécuter une fois pour indexer tous les documents
"""

from src.data_loader import load_and_split_documents
from src.vectorstore import create_and_save_vectorstore
from src.config import DATA_DIR, VECTORSTORE_DIR


def build_vectorstore():
    """
    Construit et sauvegarde la base vectorielle à partir des documents
    """
    print("="*60)
    print("🏗️  CONSTRUCTION DE LA BASE VECTORIELLE")
    print("="*60)
    
    # Étape 1 : Charger et découper les documents
    print(f"\n📂 Étape 1/2 : Chargement des documents depuis {DATA_DIR}")
    chunks = load_and_split_documents(DATA_DIR)
    
    if not chunks:
        print("❌ Aucun document trouvé !")
        print(f"💡 Ajoutez des documents PDF, DOCX ou TXT dans {DATA_DIR}")
        return False
    
    print(f"✅ {len(chunks)} chunks prêts pour l'indexation")
    
    # Étape 2 : Créer et sauvegarder la base vectorielle
    print(f"\n🗄️  Étape 2/2 : Création de la base vectorielle")
    create_and_save_vectorstore(chunks, VECTORSTORE_DIR)
    
    print("\n" + "="*60)
    print("✅ BASE VECTORIELLE CONSTRUITE AVEC SUCCÈS")
    print("="*60)
    print(f"📍 Emplacement : {VECTORSTORE_DIR}")
    print(f"📊 Nombre de chunks indexés : {len(chunks)}")
    print("\n💡 Vous pouvez maintenant lancer l'application Streamlit !")
    
    return True


if __name__ == "__main__":
    build_vectorstore()
