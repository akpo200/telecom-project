"""
Interface Streamlit pour le système RAG Télécom
Application web pour interroger la base de connaissances
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Ajouter le dossier parent au path pour importer les modules src
sys.path.append(str(Path(__file__).parent.parent))

from src.rag_pipeline import RAGPipeline
from src.config import COLORS, VECTORSTORE_DIR

# Configuration de la page
st.set_page_config(
    page_title="YAS - Assistant Intelligent RAG",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec charte YAS et animations premium
st.markdown(f"""
    <style>
    /* Gradient background for sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['primary']} 0%, #4B1D6F 100%);
        color: white;
    }}
    [data-testid="stSidebar"] .stMarkdown {{
        color: white;
    }}
    
    .main {{
        background-color: {COLORS['background']};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Premium Button Style */
    .stButton>button {{
        background: linear-gradient(90deg, {COLORS['primary']} 0%, #8E44AD 100%);
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(107, 45, 143, 0.3);
    }}
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(107, 45, 143, 0.5);
        background: {COLORS['secondary']};
        color: white;
    }}
    
    /* Chat Bubble Styles */
    .source-box {{
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid {COLORS['secondary']};
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    
    .answer-box {{
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #E0E0E0;
        margin-bottom: 25px;
        line-height: 1.6;
    }}
    
    .header-container {{
        text-align: center;
        padding: 20px 0;
        margin-bottom: 40px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }}
    
    .header-title {{
        color: {COLORS['primary']};
        font-size: 2.8em;
        font-weight: 800;
        margin-bottom: 5px;
    }}
    
    .header-subtitle {{
        color: #7F8C8D;
        font-size: 1.2em;
        letter-spacing: 1px;
    }}
    
    /* Stats cards */
    .stat-card {{
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }}
    </style>
""", unsafe_allow_html=True)


def initialize_pipeline():
    """
    Initialise le pipeline RAG
    """
    if 'pipeline' not in st.session_state:
        with st.spinner("🔄 Initialisation de l'intelligence YAS..."):
            try:
                st.session_state.pipeline = RAGPipeline()
                st.session_state.pipeline_ready = True
            except Exception as e:
                st.error(f"❌ Erreur d'initialisation : {e}")
                st.session_state.pipeline_ready = False


def display_header():
    """
    En-tête premium avec Logo
    """
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        logo_path = Path(__file__).parent / "assets" / "logo.png"
        if logo_path.exists():
            st.image(str(logo_path), width=180)
        
        st.markdown(f"""
            <div class="header-container">
                <div class="header-title">Assistant Intelligent RAG</div>
                <div class="header-subtitle">Propulsé par YAS • Base de Connaissances Interne</div>
            </div>
        """, unsafe_allow_html=True)


def display_sidebar():
    """
    Barre latérale stylisée
    """
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Centre de Contrôle")
        
        # Paramètres de recherche
        top_k = st.slider(
            "Sensibilité de recherche (Top-K)",
            min_value=1,
            max_value=10,
            value=5,
            help="Nombre de fragments de documents analysés pour chaque réponse"
        )
        
        st.markdown("---")
        st.markdown("### 📊 État du Système")
        
        # Status cards
        if VECTORSTORE_DIR.exists():
            st.markdown('<div class="stat-card">🟢 Base Vectorielle Active</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="stat-card">🔴 Base Non Trouvée</div>', unsafe_allow_html=True)
            
        if st.session_state.get('pipeline_ready', False):
            st.markdown('<div class="stat-card">🟢 IA Connectée (Cloud/Local)</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="stat-card">🟠 IA En Attente...</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 💡 Suggestions")
        
        example_questions = [
            "Quels sont les Pass Liberté ?",
            "Comment configurer l'APN manuellement ?",
            "Quelles sont les conditions de résliation ?",
            "Prix du forfait Business Premium ?"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"ex_{question}", use_container_width=True):
                st.session_state.current_question = question
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("💡 **Astuce** : Soyez précis dans vos questions pour obtenir de meilleures citations.")


def display_main_interface():
    """
    Interface de chat principale
    """
    # Zone de saisie
    question = st.text_input(
        "Comment puis-je vous aider aujourd'hui ?",
        placeholder="Ex: Quelle est la procédure pour résilier un contrat Business ?",
        key="question_input",
        value=st.session_state.get('current_question', '')
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        search_button = st.button("🚀 Interroger l'IA", use_container_width=True)
    
    if (search_button or st.session_state.get('current_question')) and question:
        with st.spinner("🔍 Analyse de la documentation en cours..."):
            try:
                # Interrogation du pipeline
                result = st.session_state.pipeline.query(question)
                
                # Réponse stylisée
                st.markdown(f"""
                    <div class="answer-box">
                        <h3 style='color: {COLORS['primary']};'>💬 Réponse de l'Assistant</h3>
                        {result['answer']}
                    </div>
                """, unsafe_allow_html=True)
                
                # Sources avec expanders premium
                if result['sources']:
                    st.markdown("### 📚 Sources Documentaires")
                    for i, doc in enumerate(result['sources'], 1):
                        source_name = Path(doc.metadata.get('source', 'Document')).name
                        page = doc.metadata.get('page', 'N/A')
                        
                        with st.expander(f"📄 [{i}] {source_name} • Page {page}"):
                            st.markdown(f"**Extrait pertinent :**")
                            st.info(doc.page_content)
                            st.caption(f"Source : {doc.metadata.get('source')}")
                
                # Feedback discret
                cols = st.columns([5, 1, 1])
                with cols[1]: st.button("👍", key="up")
                with cols[2]: st.button("👎", key="down")
                
            except Exception as e:
                st.error(f"⚠️ Une erreur est survenue : {e}")
    
    # Reset question
    if 'current_question' in st.session_state:
        st.session_state.current_question = None


def main():
    """
    Fonction principale
    """
    display_header()
    initialize_pipeline()
    display_sidebar()
    
    if not st.session_state.get('pipeline_ready', False):
        st.warning("⚠️ Le système d'intelligence n'est pas encore prêt. Vérifiez les logs.")
        return
        
    display_main_interface()


if __name__ == "__main__":
    main()
