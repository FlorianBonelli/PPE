import streamlit as st
import pandas as pd

# ==========================================
# TABEXPLORE V2 - SLEEK & FUTURISTIC
# ==========================================

# Configuration de la page
st.set_page_config(
    page_title="TabExplore - Modern Interface",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialisation de la session
if 'doc_type' not in st.session_state:
    st.session_state.doc_type = "CSV"
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'response' not in st.session_state:
    st.session_state.response = None
if 'show_upload' not in st.session_state:
    st.session_state.show_upload = False

# CSS POUR UN STYLE ÉPURÉ ET FUTURISTE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    /* Fond dégradé très doux */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        color: #1a1a1a !important;
    }

    /* Conteneur principal */
    .block-container {
        padding-top: 3rem !important;
        max-width: 800px !important;
    }

    /* Titre futuriste et épuré */
    .main-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 700;
        letter-spacing: -2px;
        color: #000000 !important;
        margin-bottom: 0px !important;
    }
    
    .main-header p {
        color: #6b7280;
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: 0px !important;
    }

    /* Stylisation des inputs Streamlit */
    .stTextInput input, .stTextArea textarea {
        border-radius: 16px !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
        padding: 1rem 1.5rem !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
        background-color: white !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.1) !important;
        transform: translateY(-2px);
    }

    /* Bouton d'upload (le +) */
    .upload-btn-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: -6px; /* Ajustement vertical pour aligner avec le selectbox */
    }

    .stButton button {
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1) !important;
    }

    /* Bouton principal "Lancer" */
    .primary-btn button {
        background: linear-gradient(90deg, #6366f1, #a855f7) !important;
        color: white !important;
        width: 100% !important;
        padding: 0.75rem !important;
        font-size: 1.2rem !important;
        margin-top: 1rem;
    }
    
    .primary-btn button:hover {
        box-shadow: 0 20px 25px -5px rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-2px);
    }

    /* Sélecteur de format épuré */
    div[data-baseweb="select"] {
        border-radius: 12px !important;
        background-color: white !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
    }
    
    /* Forcer le fond blanc pour le contrôle interne du selectbox */
    div[data-baseweb="select"] > div {
        background-color: white !important;
    }

    /* Carte de réponse - Glassmorphism léger */
    .response-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 24px;
        padding: 2rem;
        margin-top: 3rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .response-card h3 {
        color: #1f2937;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }

    .response-content {
        color: #4b5563;
        line-height: 1.7;
    }

    /* File Uploader style */
    .stFileUploader {
        border: 2px dashed #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        background: white !important;
    }

</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="main-header">
    <h1>TabExplore</h1>
    <p>Explorer les données tabulaires n'as jamais été aussi simple !</p>
</div>
""", unsafe_allow_html=True)

# SÉLECTION DE FORMAT ET UPLOAD (CENTRE AU DESSUS)
with st.container():
    # Création de colonnes pour centrer le bloc
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        col_plus, col_select = st.columns([1, 4])
        with col_plus:
            st.markdown('<div class="upload-btn-container">', unsafe_allow_html=True)
            if st.button("＋", help="Uploader un nouveau fichier", key="plus_btn", use_container_width=True):
                st.session_state.show_upload = not st.session_state.show_upload
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_select:
            st.session_state.doc_type = st.selectbox(
                "Format du fichier",
                ["CSV", "Excel", "PDF", "Doc Text"],
                index=["CSV", "Excel", "PDF", "Doc Text"].index(st.session_state.doc_type),
                label_visibility="collapsed"
            )

# ZONE D'UPLOAD CONDITIONNELLE
if st.session_state.show_upload:
    types_map = {"Doc Text": ["txt"], "PDF": ["pdf"], "CSV": ["csv"], "Excel": ["xls", "xlsx"]}
    uploaded = st.file_uploader(
        f"Sélectionnez votre fichier {st.session_state.doc_type}",
        type=types_map[st.session_state.doc_type]
    )
    if uploaded:
        st.session_state.uploaded_file = uploaded
        st.success(f"Fichier '{uploaded.name}' prêt pour l'analyse.")
        st.session_state.show_upload = False

# MESSAGE DE SUCCÈS (SI FICHIER DÉJÀ CHARGÉ MAIS ZONE FERMÉE)
elif st.session_state.uploaded_file:
    st.success(f"Fichier '{st.session_state.uploaded_file.name}' prêt pour l'analyse.")

# ZONE DE QUESTION (LARGE ET MULTI-LIGNE)
user_query = st.text_area(
    "Votre question",
    placeholder="Choisissez un format de fichier et posez moi une question sur vos données...",
    label_visibility="collapsed",
    key="query_input",
    height=150
)

# BOUTON EXECUTE (LARGE)
st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
execute = st.button("Lancer l'analyse", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# TRAITEMENT ET AFFICHAGE DES RÉSULTATS
if execute:
    if not st.session_state.uploaded_file:
        st.info("Veuillez d'abord uploader un fichier avec le bouton (＋).")
    elif not user_query.strip():
        st.warning("Veuillez entrer une question pour lancer l'analyse.")
    else:
        # Simulation d'une réponse IA
        st.session_state.response = {
            "query": user_query,
            "filename": st.session_state.uploaded_file.name,
            "type": st.session_state.doc_type
        }
        st.rerun()

# AFFICHAGE DE LA CARTE DE RÉPONSE
if st.session_state.response:
    st.markdown(f"""
    <div class="response-card">
        <h3>Résultat de l’analyse</h3>
        <div class="response-content">
            <p><strong>Fichier :</strong> {st.session_state.response['filename']} ({st.session_state.response['type']})</p>
            <p><strong>Question :</strong> {st.session_state.response['query']}</p>
            <hr style="border: none; border-top: 1px solid rgba(0,0,0,0.05); margin: 1.5rem 0;">
            <p>
                L'analyse montre que vos données tabulaires sont correctement structurées. 
                Grâce au moteur de traitement futuriste de <strong>TabExplore</strong>, nous avons pu extraire les informations clés 
                pour répondre à votre problématique.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Nouvelle question", type="secondary"):
        st.session_state.response = None
        st.rerun()

# FOOTER DISCRET
st.markdown("""
<div style="text-align: center; color: #adb5bd; font-size: 0.8rem; margin-top: 5rem;">
    TabExplore • ECE 2026
</div>
""", unsafe_allow_html=True)