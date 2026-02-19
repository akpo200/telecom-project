"""
Module du pipeline RAG complet
Orchestre l'ensemble du processus : recherche + génération
"""

from typing import List, Dict
# from langchain.chains import RetrievalQA (unused)
from langchain_core.prompts import PromptTemplate
from src.vectorstore import load_vectorstore
from src.llm import get_llm, create_rag_prompt
from src.config import TOP_K_RETRIEVAL, VECTORSTORE_DIR


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
        
        # Charger la base vectorielle (avec auto-construction si nécessaire)
        from src.config import VECTORSTORE_DIR
        print(f"📚 Chargement de la base vectorielle...")
        if not VECTORSTORE_DIR.exists() or not list(VECTORSTORE_DIR.glob("*.faiss")):
            print("⚠️ Base vectorielle manquante. Construction en cours...")
            from src.build_vectorstore import build_vectorstore
            build_vectorstore()
            
        self.vectorstore_manager = load_vectorstore()
        self.retriever = self.vectorstore_manager.get_retriever(k=top_k)
        
        # Charger le LLM
        print(f"🤖 Chargement du LLM...")
        self.llm = get_llm()
        
        print(f"✅ Pipeline RAG initialisé avec succès")
    
    def _format_prompt(self, context: str, question: str, history: List[Dict] = None) -> str:
        """
        Crée le prompt pour le RAG avec historique
        """
        history_text = ""
        if history:
            for msg in history[-6:]:  # Prendre les 3 derniers tours (user+assistant)
                role = "Client" if msg["role"] == "user" else "YAS"
                history_text += f"{role}: {msg['content']}\n"
        
        prompt = f"""[INSTRUCTION]
Vous êtes l'Assistant Virtuel de YAS (Télécom Sénégal), expert, chaleureux et professionnel.
Votre rôle est d'agir comme un véritable agent du service client.

RÈGLES D'OR :
1. Basez-vous UNIQUEMENT sur le [CONTEXTE] pour répondre.
2. Si l'info n'est pas là, redirigez poliment vers le 200. N'inventez JAMAIS de tarifs ou de procédures.
3. Rapportez-vous à l'HISTORIQUE ci-dessous si le client pose une question de suivi (ex: "Et le prix ?").
4. Style : Premium, empathique, structuré.

HISTORIQUE RÉCENT :
{history_text if history_text else "Premier contact."}

[CONTEXTE]
{context}

[QUESTION CLIENT]
{question}

[RÉPONSE SERVICE CLIENT]
"""
        return prompt
    
    def query(self, question: str, history: List[Dict] = None) -> Dict:
        """
        Pose une question au système RAG avec historique
        
        Args:
            question: Question de l'utilisateur
            history: Liste de dictionnaires {"role": "user"/"assistant", "content": "..."}
            
        Returns:
            Dictionnaire contenant la réponse et les sources
        """
        print(f"\n❓ Question : {question}")
        
        try:
            # 1. Recherche des documents pertinents
            source_documents = self.retriever.invoke(question)
            
            # 2. Préparation du contexte
            context = "\n\n".join([doc.page_content for doc in source_documents])
            
            # 3. Création du prompt
            prompt = self._format_prompt(context, question, history)
            
            # 4. Génération de la réponse
            if self.llm is None:
                answer = "Le service d'IA (LLM) est actuellement indisponible. Veuillez vérifier la connexion ou les clés API."
            elif hasattr(self.llm, "invoke"):
                response = self.llm.invoke(prompt)
                answer = response.content if hasattr(response, "content") else str(response)
            else:
                answer = self.llm(prompt)
            
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
    
    def query_with_details(self, question: str, history: List[Dict] = None) -> Dict:
        """
        Pose une question et retourne des détails enrichis
        """
        result = self.query(question, history)
        
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
        Formate la réponse pour affichage (Sans les sources pour la visibilité)
        """
        return result['answer']


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
