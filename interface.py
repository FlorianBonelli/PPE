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
        --accent-blue-soft: #dbeafe;
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
        padding-top: 4rem !important;
        padding-bottom: 6rem !important;
        max-width: 90rem !important;
    }
    
    .section-spacing {
        margin-bottom: 2.5rem;
    }
    
    .compact-header {
        text-align: center;
        padding: 0.5rem 0 2rem 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.5rem;
    }
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .subtitle {
        font-size: 1.05rem;
        color: var(--text-secondary);
        margin-top: 0.35rem;
        font-weight: 500;
    }

    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .info-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 1.25rem;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    }

    .info-card span {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--text-secondary);
    }

    .info-card h3 {
        margin: 0.35rem 0 0 0;
        font-size: 2rem;
        color: var(--text-primary);
    }

    .info-card small {
        color: var(--text-secondary);
    }

    .stButton button {
        border-radius: 999px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: none;
        background: linear-gradient(120deg, #1e3a8a, #3b82f6);
        color: #ffffff;
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.25);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 15px 30px rgba(30, 58, 138, 0.35);
    }

    div[data-testid="stTextInput"] {
        background: transparent !important;
        border: none !important;
        padding: 0;
        margin: 0;
    }

    div[data-testid="stTextInput"] input {
        height: 3.4rem;
        font-size: 1.05rem;
        border-radius: 999px;
        border: 1.5px solid var(--accent-blue-soft);
        padding: 0 1.5rem 0 2rem;
        box-shadow: inset 0 0 0 1px rgba(30, 64, 175, 0.05);
        background-color: #ffffff;
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: var(--accent-blue);
        box-shadow: inset 0 0 0 1px rgba(30, 64, 175, 0.1), 0 20px 45px rgba(30, 64, 175, 0.12);
    }

    div[data-testid="stFileUploader"] section {
        border: none;
        background: transparent;
        padding: 0;
        box-shadow: none;
    }

    div[data-testid="stSlider"] {
        padding: 0;
        margin: 0;
        background: transparent;
        border: none;
    }

    div[data-testid="stSlider"] > div {
        padding: 0;
        margin: 0;
        background: transparent;
    }

    div[role="slider"] {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        border-radius: 999px;
        height: 6px;
    }

    .mode-shell {
        padding: 0.5rem 1rem 0.75rem;
    }

    .section-gap {
        height: 9rem;
        margin: 2rem 0;
    }

    .bottom-search-shell {
        position: sticky;
        bottom: 1.5rem;
        width: calc(100% - 4rem);
        margin: 0 auto;
        z-index: 90;
    }

    .bottom-search-bar {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.4rem 1rem;
        box-shadow: 0 25px 45px rgba(15, 23, 42, 0.12);
        display: flex;
        align-items: center;
        gap: 0.45rem;
        backdrop-filter: blur(10px);
    }

    .bottom-search-bar input {
        background: transparent;
        border: none;
        outline: none !important;
        width: 100%;
        font-size: 1rem;
        color: var(--text-primary);
        padding: 0;
        text-align: center;
        line-height: 2rem;
    }

    .bottom-search-bar .stButton button {
        background: linear-gradient(120deg, #1e3a8a, #3b82f6);
        border-radius: 999px;
        padding: 0.55rem 1.4rem;
        border: none;
        font-weight: 600;
        box-shadow: 0 12px 30px rgba(30, 58, 138, 0.25);
    }

    .bottom-search-bar .icon-button button {
        background: transparent;
        border: none;
        font-size: 1.35rem;
        color: var(--accent-blue);
        display: flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        min-width: 42px;
        padding: 0;
    }

    .mini-upload {
        margin-top: 0.85rem;
        padding: 1rem;
        border-radius: 1rem;
        border: 1px dashed var(--accent-blue-soft);
        background: var(--bg-secondary);
        font-size: 0.95rem;
        color: var(--text-secondary);
    }

    .precision-panel {
        margin-top: 0.85rem;
        padding: 1rem;
        border-radius: 1rem;
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    }

    .precision-highlight {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.35rem;
    }

    .precision-note {
        color: var(--text-secondary);
        font-size: 0.9rem;
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
if "show_upload_panel" not in st.session_state:
    st.session_state.show_upload_panel = False
if "show_precision_panel" not in st.session_state:
    st.session_state.show_precision_panel = False

# Header compact
st.markdown("""
<div class="compact-header">
    <div class="main-title">TabExplorer</div>
    <div class="subtitle">recherchez vos données grace à l'intelligence artificielle</div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------
# ⚡️ BANDEAU D'INDICATEURS
# --------------------------------------------------------------------

last_file = st.session_state.uploaded_files[-1].name if st.session_state.uploaded_files else "Aucun import"
stats_container = st.container()
with stats_container:
    st.markdown(
        f"""
        <div class="info-grid">
            <div class="info-card">
                <span>Fichiers importés</span>
                <h3>{len(st.session_state.uploaded_files)}</h3>
                <small>Total disponible</small>
            </div>
            <div class="info-card">
                <span>Mode actif</span>
                <h3>{st.session_state.mode.capitalize()}</h3>
                <small>Basculer via les boutons</small>
            </div>
            <div class="info-card">
                <span>Dernier fichier</span>
                <h3 style="font-size:1.2rem;">{last_file}</h3>
                <small>Dernière référence</small>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------
# 🔧 BOUTONS + BARRE DE RECHERCHE + UPLOAD
# --------------------------------------------------------------------

interaction_zone = st.container()
with interaction_zone:

    st.markdown("<div class='mode-shell'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        btn_cols = st.columns([1, 1])
        with btn_cols[0]:
            if st.button("📤 Mode insertion", key="btn_insertion"):
                st.session_state.mode = "insertion"
                st.rerun()
        with btn_cols[1]:
            if st.button("🔎 Mode recherche", key="btn_recherche"):
                st.session_state.mode = "recherche"
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

bottom_shell = st.container()
with bottom_shell:
    st.markdown("<div class='bottom-search-shell'>", unsafe_allow_html=True)
    search_cols = st.columns([4, 0.6, 0.6, 1.4])
    with search_cols[0]:
        quick_msg = st.text_input(
            "Message rapide",
            placeholder="Posez une question ou décrivez ce que vous cherchez...",
            key="quick_input",
            label_visibility="collapsed",
        )
    with search_cols[1]:
        if st.button("➕", key="toggle_upload_panel", help="Ajouter un document"):
            st.session_state.show_upload_panel = not st.session_state.show_upload_panel
    with search_cols[2]:
        if st.button("🎯", key="toggle_precision_panel", help="Ajuster la précision"):
            st.session_state.show_precision_panel = not st.session_state.show_precision_panel
    with search_cols[3]:
        if st.button("Envoyer", key="quick_send"):
            if quick_msg:
                st.session_state.messages.append({"role": "user", "content": quick_msg})
                st.session_state.quick_input = ""
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.show_upload_panel:
        st.markdown("<div class='mini-upload'>", unsafe_allow_html=True)
        st.markdown("<strong>Glissez & déposez vos fichiers</strong>", unsafe_allow_html=True)
        mini_upload = st.file_uploader(
            "Glisser vos fichiers",
            type=["jpeg", "jpg", "png", "pdf", "txt"],
            label_visibility="collapsed",
            key="mini_upload",
        )
        if mini_upload and mini_upload not in st.session_state.uploaded_files:
            st.session_state.uploaded_files.append(mini_upload)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.show_precision_panel:
        st.markdown("<div class='precision-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='precision-highlight'>Réglage de précision</div>", unsafe_allow_html=True)
        st.session_state.precision = st.slider(
            "",
            30,
            90,
            st.session_state.precision,
            1,
            key="precision_adjust",
        )
        st.markdown(
            "<div class='precision-note'>Plus haut : réponses plus précises.</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
