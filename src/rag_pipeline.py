"""
Module du pipeline RAG complet
Orchestre l'ensemble du processus : recherche + génération
"""

from typing import List, Dict
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.vectorstore import load_vectorstore
from src.llm import get_llm, create_rag_prompt
from src.config import TOP_K_RETRIEVAL


class RAGPipeline:
    """
    Classe principale orchestrant le pipeline RAG complet
    """
    
    def __init__(self, top_k: int = TOP_K_RETRIEVAL):
        """
        Initialise le pipeline RAG
        
        Args:
            top_k: Nombre de documents à récupérer lors de la recherche
        """
        self.top_k = top_k
        
        print(f"🚀 Initialisation du pipeline RAG (top-k={top_k})")
        
        # Charger la base vectorielle
        print(f"📚 Chargement de la base vectorielle...")
        self.vectorstore_manager = load_vectorstore()
        self.retriever = self.vectorstore_manager.get_retriever(k=top_k)
        
        # Charger le LLM
        print(f"🤖 Chargement du LLM...")
        self.llm = get_llm()
        
        # Créer le template de prompt
        self.prompt_template = self._create_prompt_template()
        
        # Créer la chaîne RetrievalQA
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",  # "stuff" = tout le contexte dans un seul prompt
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )
        
        print(f"✅ Pipeline RAG initialisé avec succès")
    
    def _create_prompt_template(self) -> PromptTemplate:
        """
        Crée le template de prompt pour le RAG
        
        Returns:
            PromptTemplate LangChain
        """
        template = """[INSTRUCTION]
Tu es un assistant intelligent pour une entreprise de télécommunication au Sénégal.
Ta mission est de répondre aux questions des employés en te basant UNIQUEMENT sur les documents internes fournis ci-dessous.

RÈGLES IMPORTANTES :
- Réponds en français de manière claire et professionnelle
- Base-toi UNIQUEMENT sur le contexte fourni
- Si l'information n'est pas dans le contexte, dis "Je ne trouve pas cette information dans les documents disponibles"
- Cite toujours la source de l'information (nom du document)
- Sois précis et factuel
- Structure ta réponse avec des listes à puces ou numérotées si approprié

[CONTEXTE]
{context}

[QUESTION]
{question}

[RÉPONSE]
"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def query(self, question: str) -> Dict:
        """
        Pose une question au système RAG
        
        Args:
            question: Question de l'utilisateur
            
        Returns:
            Dictionnaire contenant la réponse et les sources
        """
        print(f"\n❓ Question : {question}")
        
        try:
            # Exécuter la chaîne RAG
            result = self.qa_chain({"query": question})
            
            # Extraire la réponse et les sources
            answer = result["result"]
            source_documents = result["source_documents"]
            
            print(f"✅ Réponse générée avec {len(source_documents)} sources")
            
            return {
                "question": question,
                "answer": answer,
                "sources": source_documents
            }
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération de la réponse : {e}")
            return {
                "question": question,
                "answer": f"Erreur : {str(e)}",
                "sources": []
            }
    
    def query_with_details(self, question: str) -> Dict:
        """
        Pose une question et retourne des détails enrichis
        
        Args:
            question: Question de l'utilisateur
            
        Returns:
            Dictionnaire avec réponse, sources et métadonnées détaillées
        """
        result = self.query(question)
        
        # Enrichir avec les détails des sources
        sources_details = []
        for doc in result["sources"]:
            sources_details.append({
                "content": doc.page_content,
                "metadata": doc.metadata
            })
        
        result["sources_details"] = sources_details
        
        return result
    
    def format_response(self, result: Dict) -> str:
        """
        Formate la réponse pour affichage
        
        Args:
            result: Résultat du query()
            
        Returns:
            Réponse formatée en texte
        """
        formatted = f"**Question :** {result['question']}\n\n"
        formatted += f"**Réponse :**\n{result['answer']}\n\n"
        
        if result['sources']:
            formatted += f"**Sources ({len(result['sources'])}) :**\n"
            for i, doc in enumerate(result['sources'], 1):
                source_name = doc.metadata.get('source', 'Document inconnu')
                page = doc.metadata.get('page', 'N/A')
                formatted += f"{i}. {source_name} (Page {page})\n"
                formatted += f"   Extrait : {doc.page_content[:150]}...\n\n"
        
        return formatted


# Fonction utilitaire pour utilisation rapide
def ask_question(question: str) -> Dict:
    """
    Fonction utilitaire pour poser une question rapidement
    
    Args:
        question: Question de l'utilisateur
        
    Returns:
        Dictionnaire avec réponse et sources
    """
    pipeline = RAGPipeline()
    return pipeline.query(question)


if __name__ == "__main__":
    # Test du module
    print("🧪 Test du pipeline RAG")
    
    try:
        # Initialiser le pipeline
        pipeline = RAGPipeline()
        
        # Poser une question de test
        test_question = "Quelles sont les principales offres disponibles ?"
        result = pipeline.query(test_question)
        
        # Afficher le résultat formaté
        print("\n" + "="*60)
        print(pipeline.format_response(result))
        print("="*60)
        
    except Exception as e:
        print(f"❌ Le test a échoué : {e}")
        print(f"💡 Assurez-vous que :")
        print(f"   1. Ollama est démarré : ollama serve")
        print(f"   2. Le modèle mistral est téléchargé : ollama pull mistral")
        print(f"   3. La base vectorielle existe (exécutez build_vectorstore.py)")
