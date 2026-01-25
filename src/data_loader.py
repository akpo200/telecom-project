"""
Module de chargement et découpage des documents
Gère l'ingestion de PDF, DOCX, TXT et leur découpage en chunks
"""

from pathlib import Path
from typing import List
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from src.config import CHUNK_SIZE, CHUNK_OVERLAP, DATA_DIR


class DocumentLoader:
    """
    Classe pour charger et découper les documents en chunks
    """
    
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        """
        Initialise le loader avec les paramètres de découpage
        
        Args:
            chunk_size: Taille des chunks en caractères
            chunk_overlap: Chevauchement entre chunks en caractères
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialiser le text splitter avec stratégie récursive
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]  # Découpe par paragraphes, puis phrases, puis mots
        )
        
        print(f"📄 DocumentLoader initialisé (chunk_size={chunk_size}, overlap={chunk_overlap})")
    
    def load_single_document(self, file_path: Path) -> List[Document]:
        """
        Charge un seul document selon son extension
        
        Args:
            file_path: Chemin vers le fichier
            
        Returns:
            Liste de documents LangChain
        """
        file_extension = file_path.suffix.lower()
        
        try:
            # Sélectionner le loader approprié selon l'extension
            if file_extension == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif file_extension == ".docx":
                loader = Docx2txtLoader(str(file_path))
            elif file_extension == ".txt":
                loader = TextLoader(str(file_path), encoding="utf-8")
            else:
                print(f"⚠️ Extension non supportée : {file_extension}")
                return []
            
            # Charger le document
            documents = loader.load()
            print(f"✅ Chargé : {file_path.name} ({len(documents)} pages)")
            return documents
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement de {file_path.name}: {e}")
            return []
    
    def load_documents_from_directory(self, directory: Path = DATA_DIR) -> List[Document]:
        """
        Charge tous les documents d'un dossier (récursif)
        
        Args:
            directory: Chemin vers le dossier contenant les documents
            
        Returns:
            Liste de tous les documents chargés
        """
        all_documents = []
        supported_extensions = [".pdf", ".docx", ".txt"]
        
        # Parcourir récursivement le dossier
        for file_path in directory.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                docs = self.load_single_document(file_path)
                all_documents.extend(docs)
        
        print(f"📚 Total de documents chargés : {len(all_documents)}")
        return all_documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Découpe les documents en chunks
        
        Args:
            documents: Liste de documents à découper
            
        Returns:
            Liste de chunks (documents découpés)
        """
        chunks = self.text_splitter.split_documents(documents)
        print(f"✂️ Documents découpés en {len(chunks)} chunks")
        return chunks
    
    def load_and_split(self, directory: Path = DATA_DIR) -> List[Document]:
        """
        Charge et découpe tous les documents d'un dossier (méthode tout-en-un)
        
        Args:
            directory: Chemin vers le dossier contenant les documents
            
        Returns:
            Liste de chunks prêts pour l'indexation
        """
        print(f"🔄 Chargement et découpage des documents depuis {directory}")
        
        # Charger tous les documents
        documents = self.load_documents_from_directory(directory)
        
        if not documents:
            print("⚠️ Aucun document trouvé !")
            return []
        
        # Découper en chunks
        chunks = self.split_documents(documents)
        
        return chunks


# Fonction utilitaire pour utilisation directe
def load_and_split_documents(directory: Path = DATA_DIR) -> List[Document]:
    """
    Fonction utilitaire pour charger et découper les documents
    
    Args:
        directory: Chemin vers le dossier contenant les documents
        
    Returns:
        Liste de chunks prêts pour l'indexation
    """
    loader = DocumentLoader()
    return loader.load_and_split(directory)


if __name__ == "__main__":
    # Test du module
    print("🧪 Test du module data_loader")
    loader = DocumentLoader()
    chunks = loader.load_and_split()
    
    if chunks:
        print(f"\n📊 Exemple de chunk :")
        print(f"Contenu : {chunks[0].page_content[:200]}...")
        print(f"Métadonnées : {chunks[0].metadata}")
