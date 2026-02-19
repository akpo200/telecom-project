"""
YAS - Assistant Client Intelligent (RAG)
Interface Premium pour le Service Client Yas Télécom
"""

import streamlit as st
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour importer les modules src
sys.path.append(str(Path(__file__).parent.parent))

from src.rag_pipeline import RAGPipeline
from src.config import COLORS, VECTORSTORE_DIR

# Initialisation de la page
st.set_page_config(
    page_title="YAS - Service Client IA",
    page_icon="💜",
    layout="wide",
)

# --- DESIGN SYSTEM PREMIUM ---
def apply_premium_style():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Arrière-plan dégradé subtil */
    .stApp {{
        background: radial-gradient(circle at top right, #FFFFFF 0%, #F8F4FF 100%);
    }}
    
    /* Sidebar premium */
    section[data-testid="stSidebar"] {{
        background-color: {COLORS['primary']} !important;
        color: white !important;
    }}
    
    /* Forcer la couleur blanche pour TOUS les textes de la sidebar */
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] h4, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {{
        color: white !important;
    }}

    /* Boutons de la sidebar */
    section[data-testid="stSidebar"] .stButton>button {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        transition: all 0.3s ease;
    }}
    
    section[data-testid="stSidebar"] .stButton>button:hover {{
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-color: white !important;
    }}
    
    /* Bulles de chat inversées - Style Premium */
    .stChatMessage {{
        padding: 1.5rem !important;
        border-radius: 20px !important;
        margin-bottom: 1rem !important;
        animation: fadeIn 0.5s ease-in-out;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    /* Style Utilisateur */
    div[data-testid="chatAvatarUser"] + div {{
        background-color: white !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 20px 20px 0 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        color: #333 !important;
    }}
    
    /* Style Assistant (YAS) */
    div[data-testid="chatAvatarAssistant"] + div {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, #4B1D6F 100%) !important;
        color: white !important;
        border-radius: 15px 15px 15px 0 !important;
        box-shadow: 0 10px 30px rgba(107, 45, 143, 0.2) !important;
    }}
    
    div[data-testid="chatAvatarAssistant"] + div p,
    div[data-testid="chatAvatarAssistant"] + div h1,
    div[data-testid="chatAvatarAssistant"] + div h2,
    div[data-testid="chatAvatarAssistant"] + div h3 {{
        color: white !important;
    }}

    /* Input fixe en bas avec style pill */
    .stChatInput {{
        border-radius: 30px !important;
        border: 1px solid {COLORS['primary']}44 !important;
        box-shadow: 0 -10px 25px rgba(0,0,0,0.03) !important;
    }}
    
    /* Badges de statut */
    .status-badge {{
        padding: 8px 16px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 10px;
        display: inline-block;
        border: 1px solid rgba(255,255,255,0.2);
    }}
    .online {{ background: #D4EDDA; color: #155724; }}
    .error {{ background: #F8D7DA; color: #721C24; }}

    /* Titres */
    .title-gradient {{
        background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['secondary']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
        letter-spacing: -1px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIQUE RAG ---
@st.cache_resource
def get_pipeline():
    try:
        return RAGPipeline()
    except Exception as e:
        st.error(f"⚠️ Erreur système : {e}")
        return None

def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Bonjour ! Je suis votre conseiller virtuel YAS. 💜\n\nJe suis à votre entière disposition pour vous guider à travers nos offres mobiles, internet et services YAS Money.\n\n**Comment puis-je vous accompagner aujourd'hui ?**"
        }]

# --- COMPOSANTS UI ---
def header():
    st.markdown('<h1 class="title-gradient">Service Client YAS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6c757d; font-size:1.2rem; margin-top:-10px;">Votre assistance intelligente, toujours à vos côtés.</p>', unsafe_allow_html=True)
    st.markdown("---")

def sidebar():
    with st.sidebar:
        from src.config import VECTORSTORE_DIR
        
        logo_path = Path(__file__).parent / "assets" / "logo.png"
        if logo_path.exists():
            st.image(str(logo_path), width=120)
        else:
            st.title("YAS")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Disponibilité")
        
        if VECTORSTORE_DIR.exists():
            st.markdown('<div class="status-badge online">🟢 Base Yas branchée</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-badge error">🔴 Base déconnectée</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="status-badge online">🟢 Intelligence Active</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 💡 Aide Rapide")
        faqs = [
            "Quels sont les différents Pass Liberté ?",
            "Configuration Internet (APN)",
            "Offres Yas Business",
            "Gestion Yas Money",
            "Code PUK bloqué"
        ]
        for q in faqs:
            if st.button(q, key=q, use_container_width=True):
                st.session_state.temp_prompt = q
                st.rerun()
        
        st.markdown("<br>"*5, unsafe_allow_html=True)
        if st.button("🗑️ Nouvelle session", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

def main_chat():
    pipeline = get_pipeline()
    
    # Zone de message (Conteneur pour forcer l'ordre)
    chat_container = st.container()

    # Gestion des questions de l'aide rapide
    if "temp_prompt" in st.session_state:
        user_input = st.session_state.pop("temp_prompt")
        st.session_state.messages.append({"role": "user", "content": user_input})
        if pipeline:
            with st.spinner("Recherche des informations..."):
                result = pipeline.query(user_input, history=st.session_state.messages[:-1])
                ans = pipeline.format_response(result)
                st.session_state.messages.append({"role": "assistant", "content": ans})
        st.rerun()

    # Affichage des messages : LE PLUS RÉCENT EN HAUT
    with chat_container:
        for msg in reversed(st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Input fixe tout en bas
    if prompt := st.chat_input("Posez votre question à YAS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        if pipeline:
            # On ne fait rien ici pour éviter l'affichage en bas, on laisse le rerun gérer
            result = pipeline.query(prompt, history=st.session_state.messages[:-1])
            ans = pipeline.format_response(result)
            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.rerun()
        else:
            st.error("Le service IA n'est pas prêt.")

# --- LANCEMENT ---
if __name__ == "__main__":
    apply_premium_style()
    init_state()
    sidebar()
    header()
    main_chat()
