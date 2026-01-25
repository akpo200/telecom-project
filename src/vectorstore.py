"""
Module de gestion de la base vectorielle FAISS
Gère l'indexation et la recherche de similarité
"""

from pathlib import Path
from typing import List
from langchain.vectorstores import FAISS
from langchain.schema import Document
from src.embeddings import get_embeddings
from src.config import VECTORSTORE_DIR


class VectorStoreManager:
    """
    Classe pour gérer la base vectorielle FAISS
    """
    
    def __init__(self, vectorstore_path: Path = VECTORSTORE_DIR):
        """
        Initialise le gestionnaire de vectorstore
        
        Args:
            vectorstore_path: Chemin où sauvegarder/charger la base vectorielle
        """
        self.vectorstore_path = vectorstore_path
        self.embeddings = get_embeddings()
        self.vectorstore = None
        
        print(f"🗄️ VectorStoreManager initialisé (path={vectorstore_path})")
    
    def create_vectorstore(self, documents: List[Document]) -> FAISS:
        """
        Crée une nouvelle base vectorielle à partir de documents
        
        Args:
            documents: Liste de documents (chunks) à indexer
            
        Returns:
            Instance FAISS vectorstore
        """
        if not documents:
            raise ValueError("❌ Aucun document fourni pour créer la base vectorielle")
        
        print(f"🔄 Création de la base vectorielle avec {len(documents)} documents...")
        
        # Créer la base vectorielle FAISS
        self.vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        print(f"✅ Base vectorielle créée avec succès")
        return self.vectorstore
    
    def save_vectorstore(self):
        """
        Sauvegarde la base vectorielle sur disque
        """
        if self.vectorstore is None:
            raise ValueError("❌ Aucune base vectorielle à sauvegarder")
        
        print(f"💾 Sauvegarde de la base vectorielle dans {self.vectorstore_path}")
        
        # Créer le dossier si nécessaire
        self.vectorstore_path.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder
        self.vectorstore.save_local(str(self.vectorstore_path))
        
        print(f"✅ Base vectorielle sauvegardée")
    
    def load_vectorstore(self) -> FAISS:
        """
        Charge une base vectorielle existante depuis le disque
        
        Returns:
            Instance FAISS vectorstore
        """
        if not self.vectorstore_path.exists():
            raise FileNotFoundError(
                f"❌ Aucune base vectorielle trouvée dans {self.vectorstore_path}"
            )
        
        print(f"🔄 Chargement de la base vectorielle depuis {self.vectorstore_path}")
        
        # Charger la base vectorielle
        self.vectorstore = FAISS.load_local(
            str(self.vectorstore_path),
            self.embeddings,
            allow_dangerous_deserialization=True  # Nécessaire pour FAISS
        )
        
        print(f"✅ Base vectorielle chargée avec succès")
        return self.vectorstore
    
    def add_documents(self, documents: List[Document]):
        """
        Ajoute de nouveaux documents à une base vectorielle existante
        
        Args:
            documents: Liste de documents à ajouter
        """
        if self.vectorstore is None:
            raise ValueError("❌ Aucune base vectorielle chargée. Créez-en une d'abord.")
        
        print(f"➕ Ajout de {len(documents)} documents à la base vectorielle")
        
        self.vectorstore.add_documents(documents)
        
        print(f"✅ Documents ajoutés avec succès")
    
    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Recherche les documents les plus similaires à une requête
        
        Args:
            query: Question/requête de l'utilisateur
            k: Nombre de documents à retourner
            
        Returns:
            Liste des k documents les plus pertinents
        """
        if self.vectorstore is None:
            raise ValueError("❌ Aucune base vectorielle chargée")
        
        print(f"🔍 Recherche de similarité pour : '{query}' (top-{k})")
        
        # Recherche de similarité
        results = self.vectorstore.similarity_search(query, k=k)
        
        print(f"✅ {len(results)} documents trouvés")
        return results
    
    def similarity_search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """
        Recherche avec scores de similarité
        
        Args:
            query: Question/requête de l'utilisateur
            k: Nombre de documents à retourner
            
        Returns:
            Liste de tuples (document, score)
        """
        if self.vectorstore is None:
            raise ValueError("❌ Aucune base vectorielle chargée")
        
        print(f"🔍 Recherche avec scores pour : '{query}' (top-{k})")
        
        # Recherche avec scores
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        print(f"✅ {len(results)} documents trouvés avec scores")
        return results
    
    def get_retriever(self, k: int = 5):
        """
        Retourne un retriever LangChain pour utilisation dans les chains
        
        Args:
            k: Nombre de documents à récupérer
            
        Returns:
            Retriever LangChain
        """
        if self.vectorstore is None:
            raise ValueError("❌ Aucune base vectorielle chargée")
        
        return self.vectorstore.as_retriever(search_kwargs={"k": k})


# Fonctions utilitaires
def create_and_save_vectorstore(documents: List[Document], path: Path = VECTORSTORE_DIR):
    """
    Fonction utilitaire pour créer et sauvegarder une base vectorielle
    
    Args:
        documents: Liste de documents à indexer
        path: Chemin de sauvegarde
    """
    manager = VectorStoreManager(path)
    manager.create_vectorstore(documents)
    manager.save_vectorstore()
    return manager


def load_vectorstore(path: Path = VECTORSTORE_DIR) -> VectorStoreManager:
    """
    Fonction utilitaire pour charger une base vectorielle existante
    
    Args:
        path: Chemin de la base vectorielle
        
    Returns:
        VectorStoreManager avec base chargée
    """
    manager = VectorStoreManager(path)
    manager.load_vectorstore()
    return manager


if __name__ == "__main__":
    # Test du module
    print("🧪 Test du module vectorstore")
    print("⚠️ Ce test nécessite des documents indexés")
