"""
YAS - Assistant Client Intelligent (RAG)
Interface Premium pour le Service Client Yas Télécom
"""

import streamlit as st
import sys
import os
from pathlib import Path
from PIL import Image

# Ajouter le dossier parent au path pour importer les modules src
sys.path.append(str(Path(__file__).parent.parent))

from src.rag_pipeline import RAGPipeline
from src.config import COLORS, VECTORSTORE_DIR

# Initialisation de la page avec un style sombre/clair automatique
st.set_page_config(
    page_title="YAS - Service Client IA",
    page_icon="💜",
    layout="wide",
)

# --- DESIGN SYSTEM ---
def apply_premium_style():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: #F8F9FA;
    }}
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background-color: {COLORS['primary']};
        color: white;
    }}
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {{
        color: white;
    }}
    
    /* Main container */
    .stApp {{
        background: radial-gradient(circle at top right, #FFFFFF 0%, #F3E5F5 100%);
    }}
    
    /* Chat messages */
    .stChatMessage {{
        background-color: transparent !important;
        padding: 1rem 0;
    }}
    
    /* User Message Bubble */
    div[data-testid="chatAvatarUser"] + div {{
        background-color: white !important;
        border-radius: 15px 15px 0 15px !important;
        border: 1px solid #E0E0E0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        padding: 1.2rem !important;
    }}
    
    /* Assistant Message Bubble */
    div[data-testid="chatAvatarAssistant"] + div {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, #4B1D6F 100%) !important;
        color: white !important;
        border-radius: 15px 15px 15px 0 !important;
        box-shadow: 0 10px 20px rgba(107, 45, 143, 0.2);
        padding: 1.2rem !important;
    }}
    
    div[data-testid="chatAvatarAssistant"] + div p {{
        color: white !important;
    }}
    
    /* Input Box */
    .stChatInput {{
        border-radius: 25px;
        box-shadow: 0 -10px 20px rgba(0,0,0,0.03);
    }}
    
    /* Status indicators */
    .status-badge {{
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 5px;
        margin-bottom: 5px;
    }}
    .status-online {{ background-color: #D4EDDA; color: #155724; border: 1px solid #C3E6CB; }}
    .status-warning {{ background-color: #FFF3CD; color: #856404; border: 1px solid #FFEEBA; }}
    
    /* Title animations */
    .hero-title {{
        background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }}
    
    .hero-subtitle {{
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }}
    
    /* Custom button styles */
    .stButton>button {{
        border-radius: 12px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .faq-btn {{
        background: white;
        border: 1px solid #E0E0E0;
        color: {COLORS['primary']};
        padding: 10px 15px;
        border-radius: 10px;
        cursor: pointer;
        margin: 5px 0;
        display: block;
        width: 100%;
        text-align: left;
        font-size: 0.9rem;
    }}
    .faq-btn:hover {{
        border-color: {COLORS['primary']};
        background: #F3E5F5;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC ---
@st.cache_resource
def get_pipeline():
    try:
        return RAGPipeline()
    except Exception as e:
        st.error(f"Erreur d'initialisation du pipeline: {e}")
        return None

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Bonjour ! Je suis l'assistant virtuel YAS. Je suis là pour vous accompagner et répondre à toutes vos questions sur nos offres et services. Comment puis-je vous aider aujourd'hui ? 😊"
        }]

# --- UI COMPONENTS ---
def display_header():
    col1, col2 = st.columns([1, 6])
    with col1:
        logo_path = Path(__file__).parent / "assets" / "logo.png"
        if logo_path.exists():
            st.image(str(logo_path), width=100)
        else:
            st.markdown(f"## 📱 **YAS**")
    
    with col2:
        st.markdown('<h1 class="hero-title">Service Client Intelligent</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">Assistance 24/7 propulsée par l\'IA generative pour plus de rapidité et de précision.</p>', unsafe_allow_html=True)

def display_sidebar():
    with st.sidebar:
        st.markdown("### 🛠️ Configuration")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Statut du système
        st.markdown("#### État du Service")
        if VECTORSTORE_DIR.exists():
            st.markdown('<div class="status-badge status-online">🟢 Base de connaissances active</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-badge status-warning">🟡 Indexation requise</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="status-badge status-online">🟢 IA Connectée</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 💡 Aide rapide")
        st.markdown("Cliquez sur une question fréquente :")
        
        faq_questions = [
            "Quels sont les différents Pass Liberté ?",
            "Comment configurer mon accès Internet (APN) ?",
            "Quelles sont les offres pour les entreprises ?",
            "Qu'est-ce que YAS Money ?",
            "Comment retrouver mon code PUK ?"
        ]
        
        for q in faq_questions:
            if st.button(q, key=q, help="Poser cette question"):
                st.session_state.temp_prompt = q
                st.rerun()

        st.markdown("---")
        if st.button("🗑️ Réinitialiser le chat", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            initialize_session_state()
            st.rerun()

def display_chat():
    pipeline = get_pipeline()
    
    # Check for temporary prompt from sidebar
    if "temp_prompt" in st.session_state:
        prompt = st.session_state.pop("temp_prompt")
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        path_to_ans = st.chat_message("assistant")
        with path_to_ans:
            with st.spinner("Je recherche les meilleures informations pour vous..."):
                result = pipeline.query(prompt)
                full_response = pipeline.format_response(result)
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Display chat history in reverse order (newest at the top)
    for msg in reversed(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input zone
    if user_prompt := st.chat_input("Dites-moi comment je peux vous aider..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Réflexion en cours..."):
                if pipeline:
                    result = pipeline.query(user_prompt, history=st.session_state.messages[:-1])
                    response = pipeline.format_response(result)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Le système d'IA n'est pas disponible. Veuillez vérifier les fichiers de configuration.")

# --- MAIN ---
def main():
    apply_premium_style()
    initialize_session_state()
    display_header()
    display_sidebar()
    
    # Layout adjustment for centering the chat
    left, middle, right = st.columns([1, 10, 1])
    with middle:
        display_chat()

if __name__ == "__main__":
    main()
