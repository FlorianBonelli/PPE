import streamlit as st
from datetime import datetime

try:
    import ia_manip  # type: ignore
except ImportError:
    ia_manip = None  # type: ignore

# Configuration de la page
st.set_page_config(
    page_title="TabExplorer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Thème moderne blanc et bleu marine - COMPACT
THEME = """
<style>
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --accent-blue: #1e40af;
        --accent-blue-light: #3b82f6;
        --text-primary: #0f172a;
        --text-secondary: #64748b;
        --border: #e2e8f0;
    }
    
    .stApp {
        background-color: var(--bg-primary);
    }
    
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    .block-container {
        padding-top: 5rem !important; /* DESCENTE DE TOUTE LA PAGE */
        padding-bottom: 1rem !important;
        max-width: 100% !important;
    }
    
    .compact-header {
        text-align: center;
        padding: 1rem 0; /* DESCENTE DU TITRE */
        margin-top: 3rem; /* DESCENTE DU TITRE */
        border-bottom: 1px solid var(--border);
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 2.6rem; /* agrandi */
        font-weight: 700;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .subtitle {
        font-size: 1rem;
        color: var(--text-secondary);
        margin-top: 0.35rem;
        font-weight: 500;
    }
</style>
"""

st.markdown(THEME, unsafe_allow_html=True)

# Initialisation
if "mode" not in st.session_state:
    st.session_state.mode = "insertion"
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "precision" not in st.session_state:
    st.session_state.precision = 50

# Header compact
st.markdown("""
<div class="compact-header">
    <div class="main-title">TabExplorer</div>
    <div class="subtitle">recherchez vos données grace à l'intelligence artificielle</div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------
# 🔧 BOUTONS CENTRÉS + BARRE DE RECHERCHE + DRAG & DROP CENTRÉ
# --------------------------------------------------------------------

center_zone = st.container()
with center_zone:

    # --- Boutons centrés ---
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        # colonnes d'espacement pour centrer les deux boutons
        spacer_l, btn_col1, btn_col2, spacer_r = st.columns([2, 1, 1, 2])
        with btn_col1:
            if st.button("📤 Insertion", key="btn_insertion"):
                st.session_state.mode = "insertion"
        with btn_col2:
            if st.button("🔎 Recherche", key="btn_recherche"):
                st.session_state.mode = "recherche"

    # --- Barre de recherche centrée (même largeur que Drag & Drop) ---
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        # Colonne centrale avec barre + bouton (bouton plus large)
        search_row = st.columns([8, 2])
        with search_row[0]:
            quick_msg = st.text_input(
                "Message rapide",
                placeholder="Tapez votre texte ici...",
                key="quick_input",
                label_visibility="collapsed"
            )
        with search_row[1]:
            if st.button("Envoyer", key="quick_send"):
                if quick_msg:
                    st.session_state.messages.append({"role": "user", "content": quick_msg})
                    st.session_state["quick_input"] = ""
                    st.rerun()

    # --- Drag & Drop ---
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        uploaded_file = st.file_uploader(
            "Fichiers",
            type=["jpeg", "jpg", "png", "pdf", "txt"],
            label_visibility="collapsed"
        )
        if uploaded_file and uploaded_file not in st.session_state.uploaded_files:
            st.session_state.uploaded_files.append(uploaded_file)
            st.rerun()

# --------------------------------------------------------------------
# 🧩 LAYOUT PRINCIPAL
# --------------------------------------------------------------------

left_col, right_col = st.columns([1.5, 1])

# COLONNE GAUCHE - Contenu principal
with left_col:

    # --- TITRE CENTRÉ SOUS LE DRAG & DROP ---
    if st.session_state.mode == "insertion":
        st.markdown("<h3 style='text-align:center'>📤 Insertion de documents</h3>", unsafe_allow_html=True)
        
        if st.session_state.uploaded_files:
            for idx, file in enumerate(st.session_state.uploaded_files):
                col_name, col_btn1, col_btn2 = st.columns([3, 1, 1])
                with col_name:
                    st.text(f"📄 {file.name}")
                with col_btn1:
                    if st.button("✅", key=f"process_{idx}"):
                        if ia_manip:
                            try:
                                if file.type in ["image/jpeg", "image/jpg", "image/png"]:
                                    ia_manip.traitement_JPEG(file)
                                    st.success("✅ Traité!")
                                elif file.type == "text/plain":
                                    ia_manip.traitement_TXT(file)
                                    st.success("✅ Traité!")
                            except Exception as e:
                                st.error(f"❌ Erreur: {str(e)}")
                        else:
                            st.error("Module manquant")
                with col_btn2:
                    if st.button("🗑️", key=f"del_{idx}"):
                        st.session_state.uploaded_files.pop(idx)
                        st.rerun()
        else:
            st.info("📥 Aucun fichier uploadé")
    
    elif st.session_state.mode == "recherche":
        st.markdown("<h3 style='text-align:center'>🔎 Recherche de documents</h3>", unsafe_allow_html=True)
        
        st.session_state.precision = st.slider(
            "Précision", 30, 90, st.session_state.precision, 1
        )
        
        if st.session_state.uploaded_files:
            file = st.session_state.uploaded_files[-1]
            st.text(f"Référence: {file.name}")
            st.text(f"Précision: {st.session_state.precision}%")
            
            if st.button("🔍 Lancer la recherche"):
                if ia_manip:
                    st.info("🔄 Recherche à implémenter")
                else:
                    st.error("Module manquant")
        else:
            st.info("📥 Uploadez un fichier de référence")

# COLONNE DROITE - Fichiers + Mode centrés
with right_col:
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center'>
        <b>Fichiers:</b> {n}<br>
        <b>Mode:</b> {mode}
    </div>
    """.format(
        n=len(st.session_state.uploaded_files),
        mode=st.session_state.mode.capitalize()
    ), unsafe_allow_html=True)
