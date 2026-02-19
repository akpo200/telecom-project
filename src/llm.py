"""
Module de gestion du modèle de langage (LLM)
Gère l'interaction avec Ollama (Mistral), Groq ou Mistral AI
"""

import os

# Imports conditionnels pour éviter les erreurs de dépendances
try:
    from langchain_community.llms import Ollama
except ImportError:
    Ollama = None

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

try:
    from langchain_mistralai import ChatMistralAI
except ImportError:
    ChatMistralAI = None

from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL, MISTRAL_API_KEY


class LLMManager:
    """
    Classe pour gérer le modèle de langage
    """
    
    def __init__(
        self, 
        model_name: str = OLLAMA_MODEL,
        base_url: str = OLLAMA_BASE_URL,
        temperature: float = 0.3,
    ):
        """
        Initialise le gestionnaire LLM
        
        Args:
            model_name: Nom du modèle
            base_url: URL de l'API (pour Ollama)
            temperature: Température de génération
        """
        self.model_name = model_name
        self.base_url = base_url
        self.temperature = temperature
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """
        Initialise le fournisseur LLM approprié
        """
        # 1. Vérifier si Groq est disponible
        groq_api_key = os.getenv("GROQ_API_KEY")
        if groq_api_key and ChatGroq:
            print("🚀 Utilisation de Groq Cloud API")
            return ChatGroq(
                api_key=groq_api_key,
                model_name="llama-3.1-8b-instant",
                temperature=self.temperature
            )

        # 2. Vérifier si Mistral AI API est disponible
        if MISTRAL_API_KEY and ChatMistralAI:
            print("🚀 Utilisation de Mistral AI API")
            return ChatMistralAI(
                api_key=MISTRAL_API_KEY,
                model="mistral-medium",
                temperature=self.temperature
            )

        # 3. Par défaut : Ollama (local)
        if Ollama:
            print(f"🤖 Utilisation d'Ollama local : {self.model_name}")
            try:
                return Ollama(
                    model=self.model_name,
                    base_url=self.base_url,
                    temperature=self.temperature
                )
            except Exception as e:
                print(f"⚠️ Erreur Ollama : {e}")
        
        # Si rien ne marche
        print("❌ Aucun moteur LLM disponible. Vérifiez les installations.")
        return None

    def generate(self, prompt: str) -> str:
        """
        Génère une réponse à partir d'un prompt
        """
        try:
            if hasattr(self.llm, "invoke"):
                response = self.llm.invoke(prompt)
                return response.content if hasattr(response, "content") else str(response)
            else:
                return self.llm(prompt)
        except Exception as e:
            print(f"❌ Erreur de génération : {e}")
            return f"Erreur : Impossible de générer une réponse. Détails : {str(e)}"
    
    def get_llm(self):
        """
        Retourne l'instance LLM pour utilisation avec LangChain
        """
        return self.llm


def create_rag_prompt(context: str, question: str) -> str:
    """
    Crée un prompt structuré pour le RAG
    """
    prompt = f"""[INSTRUCTION]
Tu es un assistant intelligent pour une entreprise de télécommunication au Sénégal nommée YAS.
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
    return prompt


# Fonction utilitaire pour obtenir le LLM
def get_llm(model_name: str = OLLAMA_MODEL, temperature: float = 0.3):
    """
    Fonction utilitaire pour obtenir une instance LLM
    """
    manager = LLMManager(model_name=model_name, temperature=temperature)
    return manager.get_llm()


if __name__ == "__main__":
    # Test du module
    print("🧪 Test du module LLM")
    try:
        manager = LLMManager()
        test_prompt = "Bonjour, peux-tu te présenter en une phrase ?"
        print(f"Réponse : {manager.generate(test_prompt)}")
    except Exception as e:
        print(f"❌ Échec : {e}")
