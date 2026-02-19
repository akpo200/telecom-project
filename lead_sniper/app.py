import streamlit as st
import pandas as pd
from lead_sniper.sniper import LeadSniper
from lead_sniper.database import save_leads, get_all_leads
import time

# Configuration de la page
st.set_page_config(
    page_title="Lead Sniper AI - Expert V3",
    page_icon="🎯",
    layout="wide"
)

# Style CSS Premium
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    .stButton>button {
        background: linear-gradient(45deg, #ff4b2b, #ff416c);
        color: white; border: none; padding: 12px 30px; border-radius: 12px; font-weight: bold; width: 100%;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.3);
    }
    .stMetric { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# Initialisation
if 'sniper' not in st.session_state:
    st.session_state.sniper = LeadSniper()

all_stored_leads = get_all_leads()

# Header
st.title("🎯 Lead Sniper AI V3 - Acquisition Massive")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚡ Lancer la Chasse")
    theme = st.selectbox("Thématique", ["Rachat de crédit", "Immobilier"])
    
    if st.button("🚀 SCAN GLOBAL : EXTRACTION PROFONDE"):
        with st.status("Extraction en cours (Scan exhaustif Google 100+ pages)...", expanded=True) as status:
            queries = st.session_state.sniper.get_queries(theme)
            new_found = []
            for q in queries:
                st.write(f"🔍 Analyse : `{q[:50]}...`")
                res = st.session_state.sniper.seo_client.search_leads(q)
                leads = st.session_state.sniper.process_search_results(theme, res)
                new_found.extend(leads)
            
            added = save_leads(new_found)
            status.update(label=f"Succès ! {added} nouveaux leads qualifiés.", state="complete")
            st.rerun()

# Statistiques
col1, col2, col3 = st.columns(3)
col1.metric("Leads en Base", len(all_stored_leads))
col2.metric("Qualité Moyenne", "Élevée (IA Checked)")
col3.metric("Potentiel Revenu", f"{len(all_stored_leads) * 50} €")

st.markdown("### 📋 Tableau de Bord des Prospects ( Exhaustif )")

if all_stored_leads:
    df = pd.DataFrame(all_stored_leads)
    
    # Mapping des colonnes pour le tableau final
    # On gère l'ancienne version des données (nom vs nom_complet)
    if 'nom_complet' not in df.columns and 'nom' in df.columns:
        df['nom_complet'] = df['nom']
    if 'date_originale_post' not in df.columns:
        df['date_originale_post'] = "Inconnue"
        
    cols_display = {
        'date_originale_post': '📅 Date Publication',
        'nom_complet': '👤 Nom Complet',
        'telephone': '📞 Téléphone',
        'email': '📧 Email',
        'type_projet': '🏠 Projet',
        'urgence': '⚡ Priorité',
        'commentaire_detaille': '💬 Détails',
        'url_source': '🔗 Source'
    }
    
    # On ne garde que les colonnes qui existent
    actual_cols = [c for c in cols_display.keys() if c in df.columns]
    df_filtered = df[actual_cols].copy()
    
    # Nettoyage des noms
    df_filtered['nom_complet'] = df_filtered['nom_complet'].replace(['Inconnu', 'inconnu', 'None', None], '🔍 À vérifier sur source')

    # Affichage
    st.dataframe(
        df_filtered.rename(columns=cols_display),
        column_config={
            "🔗 Source": st.column_config.LinkColumn("Source"),
            "📞 Téléphone": st.column_config.TextColumn("Contact Direct"),
            "📅 Date Publication": st.column_config.TextColumn("Fraîcheur"),
        },
        use_container_width=True,
        hide_index=True,
        height=600
    )
    
    st.download_button(
        "📥 EXPORTER LA LISTE POUR LEADVALUE (PRO CSV)",
        df_filtered.to_csv(index=False).encode('utf-8'),
        f"leads_premium_{theme}.csv",
        "text/csv"
    )
else:
    st.info("Aucun lead détecté. Lancez un scan global pour peupler la base.")

st.markdown("---")
st.caption("Filtre anti-fraude activé - Données extraites par Intelligence Artificielle (Llama 3.3 70B)")
