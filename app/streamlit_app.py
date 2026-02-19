"""
YAS - Assistant Client Intelligent (RAG)
Interface Premium pour le Service Client Yas Télécom
"""

import streamlit as st
import sys
import time
from pathlib import Path

# Ajouter le dossier parent au path pour importer les modules src
sys.path.append(str(Path(__file__).parent.parent))

# Importations sécurisées
try:
    from src.rag_pipeline import RAGPipeline
    from src.config import COLORS, VECTORSTORE_DIR
except ImportError as e:
    st.error(f"Erreur d'importation : {e}")
    # Fallback si l'import initial échoue à cause du path
    sys.path.append(str(Path.cwd()))
    from src.rag_pipeline import RAGPipeline
    from src.config import COLORS, VECTORSTORE_DIR

# Initialisation de la page
st.set_page_config(
    page_title="YAS Assistant - Premium",
    page_icon="💜",
    layout="wide",
)

# --- DESIGN SYSTEM ---
def apply_premium_style():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Outfit', sans-serif;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, #FFFFFF 0%, #F5F0FF 100%);
    }}
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {{
        background-color: {COLORS['primary']} !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }}
    
    section[data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    .sidebar-logo {{
        display: flex;
        justify-content: center;
        padding: 20px 0;
    }}
    
    /* Chat Bubble Styles */
    .stChatMessage {{
        background-color: transparent !important;
        padding: 1rem 0 !important;
    }}
    
    /* Bulle Assistant (YAS) */
    div[data-testid="chatAvatarAssistant"] + div {{
        background: white !important;
        color: {COLORS['text']} !important;
        border: 1px solid {COLORS['primary']}22 !important;
        border-radius: 20px 20px 20px 0px !important;
        box-shadow: 0 4px 15px rgba(107, 45, 143, 0.08) !important;
        padding: 1.2rem !important;
    }}
    
    /* Bulle Utilisateur */
    div[data-testid="chatAvatarUser"] + div {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, #4B1D6F 100%) !important;
        color: white !important;
        border-radius: 20px 20px 0px 20px !important;
        box-shadow: 0 10px 25px rgba(107, 45, 143, 0.2) !important;
        padding: 1.2rem !important;
    }}
    
    div[data-testid="chatAvatarUser"] + div p {{
        color: white !important;
    }}
    
    /* Status Badge */
    .status-badge {{
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 8px;
        display: inline-block;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }}

    /* Title Styling */
    .hero-container {{
        text-align: center;
        padding: 2rem 0;
    }}
    
    .hero-title {{
        background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0px;
    }}
    
    /* Boutique YAS vibe */
    .stChatInput {{
        border-radius: 30px !important;
        border: 1px solid {COLORS['primary']}33 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- APP LOGIC ---
@st.cache_resource
def get_pipeline():
    try:
        return RAGPipeline()
    except Exception as e:
        st.error(f"⚠️ Erreur d'initialisation : {e}")
        return None

def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "memory" not in st.session_state:
        st.session_state.memory = []

# --- COMPONENTS ---
def sidebar():
    with st.sidebar:
        logo_path = Path(__file__).parent / "assets" / "logo.png"
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        else:
            st.markdown("<h1 style='text-align:center;'>YAS</h1>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🟢 État du Service")
        st.markdown('<div class="status-badge">Base de données Yas Active</div>', unsafe_allow_html=True)
        st.markdown('<div class="status-badge">IA Conversationnelle Prête</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 💡 Suggestions")
        questions = [
            "Quels sont les Pass Liberté ?",
            "Où acheter une carte SIM ?",
            "Configuration APN Internet",
            "Frais de retrait Yas Money"
        ]
        for q in questions:
            if st.button(q, key=q, use_container_width=True):
                st.session_state.current_prompt = q
        
        st.markdown("<br>"*10, unsafe_allow_html=True)
        if st.button("🗑️ Effacer la mémoire", use_container_width=True):
            st.session_state.messages = []
            st.session_state.memory = []
            st.rerun()

def display_chat():
    pipeline = get_pipeline()
    
    # Header
    st.markdown('<div class="hero-container"><h1 class="hero-title">Comment puis-je vous aider ?</h1><p style="color:#666;">Assistant Virtuel Yas Télécom à votre service 24h/7j</p></div>', unsafe_allow_html=True)
    
    # Zone d'affichage des messages (Ordre Classique : Nouveau en bas)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Traitement des questions suggérées
    input_val = st.chat_input("Votre message ici...")
    
    final_prompt = None
    if input_val:
        final_prompt = input_val
    elif "current_prompt" in st.session_state:
        final_prompt = st.session_state.pop("current_prompt")

    if final_prompt:
        # Affichage immédiat du message utilisateur
        with st.chat_message("user"):
            st.markdown(final_prompt)
        st.session_state.messages.append({"role": "user", "content": final_prompt})
        
        # Génération de la réponse
        with st.chat_message("assistant"):
            if pipeline:
                with st.spinner("YAS réfléchit..."):
                    # On passe TOUTE l'historique pour la mémoire
                    result = pipeline.query(final_prompt, history=st.session_state.memory)
                    response = pipeline.format_response(result)
                    
                    # Simuler une frappe pour le "Wouaw"
                    placeholder = st.empty()
                    full_text = ""
                    for char in response:
                        full_text += char
                        placeholder.markdown(full_text + "▌")
                        time.sleep(0.005)
                    placeholder.markdown(full_text)
                    
                    # Mise à jour de la mémoire
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.session_state.memory.append({"role": "user", "content": final_prompt})
                    st.session_state.memory.append({"role": "assistant", "content": response})
                    
                    # Limiter la mémoire aux 10 derniers échanges
                    if len(st.session_state.memory) > 20:
                        st.session_state.memory = st.session_state.memory[-20:]
            else:
                st.error("Désolé, le cerveau de l'IA est indisponible.")

if __name__ == "__main__":
    init_session()
    apply_premium_style()
    sidebar()
    display_chat()
