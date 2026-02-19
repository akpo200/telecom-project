import os
import json
import re
from typing import List, Dict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from lead_sniper.dataforseo_client import DataForSEOClient

# Chargement des variables d'environnement
load_dotenv()

class LeadSniper:
    def __init__(self):
        # Initialisation de l'IA pour la qualification
        self.llm = ChatGroq(
            temperature=0,
            model_name="llama-3.3-70b-versatile",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.seo_client = DataForSEOClient()
        
    def get_queries(self, theme: str) -> List[str]:
        """Génère des requêtes ultra-agressives pour trouver des leads frais."""
        queries = {
            "Rachat de crédit": [
                'site:facebook.com "besoin de rachat de crédit" OR "cherche regroupement de crédits" "06" OR "07"',
                'site:twitter.com "besoin rachat" OR "cherche rachat" "06" OR "07"',
                'site:linkedin.com "rachat de crédit" "besoin" "06"',
                'site:facebook.com/groups "recherche de crédit" "aider" "06"',
                '"besoin de liquidité" "rachat de crédit" "06"',
                'forum "rachat de crédit" "contact" "06" OR "07"'
            ],
            "Immobilier": [
                'site:facebook.com "investissement Pinel" OR "LMNP" "besoin conseil" "06" OR "07"',
                'site:facebook.com "vendre mon appartement" "urgent" "06"',
                'site:twitter.com "cherche investissement immobilier" "06"',
                'site:leboncoin.fr "vends appartement" "particulier" "06"',
                '"cherche appartement" "urgent" "06" OR "07"',
                '"vendre maison" "estimation gratuite" "06"'
            ]
        }
        return queries.get(theme, [])

    def process_search_results(self, theme: str, search_results: List[Dict]) -> List[Dict]:
        """Analyse les résultats de recherche pour extraire les leads réels."""
        qualified_leads = []
        
        # On augmente la limite pour trouver plus de leads qualifiés
        for result in search_results[:30]:
            raw_text = f"Titre: {result['title']}\nSnippet: {result['snippet']}\nURL: {result['url']}"
            lead = self.qualify_lead(raw_text, theme)
            
            if lead.get("est_un_vrai_lead"):
                lead["url_source"] = result["url"]
                qualified_leads.append(lead)
                
        return qualified_leads

    def qualify_lead(self, text: str, theme: str) -> Dict:
        """Utilise l'IA pour qualifier un lead avec une précision extrême."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""Tu es un analyste de données expert en prospection pour la thématique {theme}. 
            Ta mission est d'extraire des informations CRUCIALES d'un snippet Google.
            
            Règles d'extraction :
            1. NOM : Cherche le nom complet. Ne mets pas 'Inconnu' si tu peux déduire un pseudo ou un nom de profil à partir du texte ou de l'URL.
            2. DATE DU POST : Cherche dans le texte si une date est mentionnée (ex: 'posté il y a 2h', 'le 10 juin', etc.). Si aucune date n'est mentionnée, essaie d'estimer si le message semble récent ou vieux.
            3. CONTACT : Extrais TOUS les numéros de téléphone (06/07) et emails. Nettoie les espaces.
            4. VALIDATION : Soit très strict. Un lead est vrai (TRUE) uniquement si il y a une intention d'achat/vente/besoin claire ET un moyen de contact.
            
            Rends un JSON (et rien d'autre) avec :
            - nom_complet
            - telephone
            - email
            - date_originale_post (ex: '10 juin 2025' ou 'Inconnue')
            - type_projet
            - urgence (Bas, Moyen, Haut)
            - est_un_vrai_lead (boolean)
            - commentaire_detaille
            """),
            ("user", "{text}")
        ])
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({"text": text})
            match = re.search(r'\{.*\}', response.content, re.DOTALL)
            if match:
                data = json.loads(match.group())
                # Nettoyage basique
                if "nom_complet" in data and data["nom_complet"].lower() == "inconnu":
                    # Tentative de récupération depuis le texte si possible
                    pass
                return data
        except:
            pass
        return {"est_un_vrai_lead": False}

    def run_snipe(self, theme: str):
        """Exécution complète du processus de sniping."""
        queries = self.get_queries(theme)
        all_results = []
        
        for q in queries:
            results = self.seo_client.search_leads(q)
            all_results.extend(results)
            
        return self.process_search_results(theme, all_results)
