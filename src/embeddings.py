"""
Module de génération des embeddings
Gère la transformation du texte en vecteurs sémantiques
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from src.config import EMBEDDING_MODEL


class EmbeddingManager:
    """
    Classe pour gérer la génération des embeddings
    """
    
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """
        Initialise le modèle d'embeddings
        
        Args:
            model_name: Nom du modèle HuggingFace à utiliser
        """
        self.model_name = model_name
        
        print(f"🔄 Chargement du modèle d'embeddings : {model_name}")
        
        # Initialiser le modèle HuggingFace
        # model_kwargs: Configuration pour utiliser le CPU
        # encode_kwargs: normalize_embeddings=True pour améliorer la recherche par similarité
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        print(f"✅ Modèle d'embeddings chargé avec succès")
    
    def embed_query(self, text: str) -> list:
        """
        Génère l'embedding pour une requête (question utilisateur)
        
        Args:
            text: Texte de la requête
            
        Returns:
            Vecteur d'embedding (liste de floats)
        """
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: list) -> list:
        """
        Génère les embeddings pour plusieurs documents
        
        Args:
            texts: Liste de textes à vectoriser
            
        Returns:
            Liste de vecteurs d'embeddings
        """
        return self.embeddings.embed_documents(texts)
    
    def get_embeddings_model(self):
        """
        Retourne l'objet embeddings pour utilisation avec LangChain
        
        Returns:
            Instance HuggingFaceEmbeddings
        """
        return self.embeddings


# Fonction utilitaire pour obtenir le modèle d'embeddings
def get_embeddings(model_name: str = EMBEDDING_MODEL):
    """
    Fonction utilitaire pour obtenir le modèle d'embeddings
    
    Args:
        model_name: Nom du modèle à utiliser
        
    Returns:
        Instance HuggingFaceEmbeddings
    """
    manager = EmbeddingManager(model_name)
    return manager.get_embeddings_model()


if __name__ == "__main__":
    # Test du module
    print("🧪 Test du module embeddings")
    
    manager = EmbeddingManager()
    
    # Test avec une phrase
    test_text = "Quelles sont les offres mobiles disponibles chez Orange ?"
    embedding = manager.embed_query(test_text)
    
    print(f"\n📊 Résultat du test :")
    print(f"Texte : {test_text}")
    print(f"Dimensions de l'embedding : {len(embedding)}")
    print(f"Premiers éléments : {embedding[:5]}")
