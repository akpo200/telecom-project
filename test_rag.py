
from src.rag_pipeline import RAGPipeline
import os
from dotenv import load_dotenv

def test_rag():
    print("🧪 Test du pipeline RAG en local...")
    
    # Charger les variables d'environnement
    load_dotenv()
    
    try:
        # Initialiser le pipeline
        pipeline = RAGPipeline()
        
        # Question de test
        question = "Quels sont les Pass Liberté ?"
        print(f"\n❓ Question : {question}")
        
        # Lancer la requête
        result = pipeline.query(question)
        
        # Afficher la réponse
        print("\n" + "="*60)
        print(f"💬 RÉPONSE :")
        print(result['answer'])
        print("="*60)
        
        # Afficher les sources
        if result['sources']:
            print("\n📚 SOURCES :")
            for i, doc in enumerate(result['sources'], 1):
                print(f"[{i}] {doc.metadata.get('source')} (Page {doc.metadata.get('page')})")
        
        # Sauvegarder le résultat dans un fichier
        with open("test_output.txt", "w", encoding="utf-8") as f:
            f.write(f"Question: {question}\n")
            f.write(f"Answer: {result['answer']}\n")
            f.write("\nSources:\n")
            for doc in result['sources']:
                f.write(f"- {doc.metadata.get('source')}\n")

        print("\n✅ Test terminé avec succès ! Résultat sauvegardé dans test_output.txt")
        
    except Exception as e:
        print(f"\n❌ Erreur pendant le test : {e}")

if __name__ == "__main__":
    test_rag()
