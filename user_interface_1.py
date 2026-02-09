import streamlit as st
from datetime import datetime
import pandas as pd

# ==========================================
# TABLE EXPLORE - Interface Optimisée
# ==========================================

# Configuration de la page
st.set_page_config(
    page_title="TabExplore",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialisation de la session
session_defaults = {
    'doc_type': None,
    'uploaded_file': None,
    'response': None,
    'show_upload': False
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# CSS optimisé
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    .stApp { background-color: #f5f5f5; }
    .main { max-width: 900px; padding: 3rem 2rem; }
    #MainMenu, footer, header { visibility: hidden; }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: #000000;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .main-subtitle {
        color: #666666;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* Zone de recherche avec bouton + */
    .search-wrapper {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .upload-btn-custom {
        width: 50px;
        height: 50px;
        background: transparent;
        border: none;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: #000000;
        cursor: pointer;
        transition: all 0.3s ease;
        flex-shrink: 0;
    }
    
    .upload-btn-custom:hover {
        background: #f0f0f0;
        transform: scale(1.05);
    }
    
    /* Input texte */
    .stTextInput input,
    .stTextArea textarea {
        background: #d0d0d0 !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 1.25rem 2rem !important;
        font-size: 1rem !important;
        color: #333 !important;
        resize: none !important;
    }
    
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        background: #c8c8c8 !important;
        box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder { 
        color: #888 !important; 
    }
    
    /* Boutons de format */
    div[data-testid="column"] .stButton button {
        background: white !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #000000 !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="column"] .stButton button:hover {
        border-color: #000000 !important;
        background: #f8f8f8 !important;
    }
    
    div[data-testid="column"] .stButton button:active {
        transform: scale(0.95) !important;
    }
    
    /* Style spécifique pour le bouton + */
    div[data-testid="column"]:first-child .stButton button {
        background: transparent !important;
        border: none !important;
        color: #000000 !important;
        font-size: 2rem !important;
        padding: 0 !important;
        width: 50px !important;
        height: 50px !important;
        border-radius: 50% !important;
    }
    
    div[data-testid="column"]:first-child .stButton button:hover {
        background: #f0f0f0 !important;
        border: none !important;
    }
    
    div[data-testid="column"]:first-child .stButton button:active {
        transform: scale(0.95) !important;
    }
    
    /* Bouton principal */
    .stButton button {
        background: #000000;
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: #333333;
        transform: translateY(-2px);
    }
    
    /* File uploader caché */
    .hidden-uploader {
        display: none !important;
    }
    
    /* Zone de réponse */
    .response-container {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 2rem;
        animation: fadeIn 0.4s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .response-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #000;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .response-content {
        color: #333;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem;">
    <h1 class="main-title">TabExplore</h1>
    <p class="main-subtitle">Explorer les données tabulaires n'a jamais été aussi simple qu'aujourd'hui</p>
</div>
""", unsafe_allow_html=True)

# Boutons de sélection de format
file_types_map = {
    "Doc Text": ["txt"],
    "PDF": ["pdf"],
    "CSV": ["csv"],
    "Excel": ["xls", "xlsx"]
}

col1, col2, col3, col4 = st.columns(4)

for idx, (col, doc_type) in enumerate(zip([col1, col2, col3, col4], file_types_map.keys())):
    with col:
        icon = "🔴" if st.session_state.doc_type == doc_type else "⚪"
        if st.button(f"{icon} {doc_type}", key=f"btn_{idx}", use_container_width=True):
            st.session_state.doc_type = doc_type
            st.session_state.uploaded_file = None
            st.rerun()

# Zone de saisie avec bouton + et input alignés
st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)

col_upload, col_input = st.columns([1, 15])

with col_upload:
    # Bouton + stylisé en HTML
    if st.button("➕", key="upload_toggle", help="Uploader un fichier"):
        st.session_state.show_upload = True
        # Déclencher l'upload via JavaScript serait idéal, mais Streamlit ne le permet pas directement
        # On utilise donc un file_uploader visible conditionnellement

with col_input:
    user_question = st.text_area(
        "Question",
        placeholder="Choisissez un format de document et posez-moi une question !",
        label_visibility="collapsed",
        key="question_input",
        height=100
    )

st.markdown('</div>', unsafe_allow_html=True)

# File uploader (apparaît après le clic sur +)
if st.session_state.show_upload and st.session_state.doc_type:
    uploaded_file = st.file_uploader(
        f"📎 Sélectionnez votre fichier {st.session_state.doc_type}",
        type=file_types_map[st.session_state.doc_type],
        key="file_uploader"
    )
    
    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        st.session_state.show_upload = False  # Fermer l'uploader après sélection
        
        # Aperçu selon le type
        if st.session_state.doc_type in ["CSV", "Excel"]:
            try:
                df = pd.read_csv(uploaded_file) if st.session_state.doc_type == "CSV" else pd.read_excel(uploaded_file)
                with st.expander("📊 Aperçu des données"):
                    st.dataframe(df.head(10), use_container_width=True)
                    st.caption(f"{len(df)} lignes × {len(df.columns)} colonnes")
            except Exception as e:
                st.error(f"Erreur de lecture : {e}")

elif st.session_state.show_upload and not st.session_state.doc_type:
    st.warning("⚠️ Veuillez d'abord sélectionner un format de document")

# Bouton d'envoi
if st.button("Envoyer", use_container_width=True):
    if not st.session_state.doc_type:
        st.warning("⚠️ Veuillez sélectionner un format de document")
    elif not st.session_state.uploaded_file:
        st.warning("⚠️ Veuillez uploader un fichier")
    elif not user_question.strip():
        st.warning("⚠️ Veuillez poser une question")
    else:
        st.session_state.response = {
            "question": user_question,
            "file": st.session_state.uploaded_file.name,
            "type": st.session_state.doc_type
        }
        st.rerun()

# Affichage de la réponse
if st.session_state.response:
    st.markdown('<div class="response-container">', unsafe_allow_html=True)
    st.markdown('<div class="response-title">🤖 Réponse de l\'IA</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
**Fichier analysé :** {st.session_state.response['file']} ({st.session_state.response['type']})

**Votre question :** {st.session_state.response['question']}

---

**Réponse :**

Ceci est une réponse simulée pour tester l'ergonomie de l'interface. 

Dans la version complète, l'IA analyserait votre fichier **{st.session_state.response['type']}** et fournirait une réponse détaillée basée sur le contenu réel de **{st.session_state.response['file']}**.

L'analyse inclurait :
- 📊 Extraction et traitement des données
- 🔍 Recherche d'informations pertinentes  
- 💡 Génération d'insights basés sur votre question
- 📈 Visualisations si nécessaire

*Cette interface est en mode démonstration. Les fonctionnalités d'IA complètes seront intégrées dans la version finale.*
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Nouvelle question"):
        st.session_state.response = None
        st.rerun()