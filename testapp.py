import streamlit as st

# ----------------- CONFIG -----------------
st.set_page_config(
    page_title="TabExplorer v0.1",
    page_icon="📊",
    layout="wide",
)

# ----------------- SESSION STATE -----------------
if "insert_files" not in st.session_state:
    st.session_state.insert_files = []
if "search_files" not in st.session_state:
    st.session_state.search_files = []
if "show_uploader" not in st.session_state:
    st.session_state.show_uploader = False

# ----------------- CSS -----------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2.5rem;
        max-width: 1200px;
    }

    section[data-testid="stSidebar"] {
        background-color: #f5f5f7;
        border-right: 1px solid #e5e7eb;
    }

    .tabx-title-wrapper { text-align: center; margin-bottom: 0.3rem; }
    .tabx-title {
        font-family: system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
        font-size: 2.1rem;
        font-weight: 500;
        color: #000000;
    }
    .tabx-subtitle {
        text-align: center;
        font-size: 0.95rem;
        color: #6b7280;
        margin-bottom: 1.6rem;
    }

    .tabx-section-header {
        display: flex;
        align-items: center;
        gap: .45rem;
        margin-bottom: .4rem;
        margin-top: .8rem;
    }
    .tabx-section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #111827;
    }
    .tabx-helper {
        font-size: .85rem;
        color: #6b7280;
        margin-bottom: .8rem;
    }
    .tabx-label {
        font-size: .86rem;
        font-weight: 600;
        color: #4b5563;
        margin-bottom: .25rem;
    }

    /* Champ texte en pilule (barre centrale) */
    /* Champ texte façon ChatGPT : fond blanc, bord léger, ombre douce */
    div[data-baseweb="input"] {
    border-radius: 999px !important;
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;        /* bord très léger (gris clair) */
    box-shadow: 0 4px 10px rgba(15,23,42,0.05) !important;  /* ombre plus discrète */
    padding-left: 14px !important;
    padding-right: 14px !important;
    }

    div[data-baseweb="input"] input {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: white !important;
    font-size: .95rem;
    color: #111827;
    }


    /* Boutons + et ➤ */
    .stButton > button {
        background: white !important;
        border: none !important;
        box-shadow: none !important;
        color: #111827 !important;
        width: 34px !important;
        height: 34px !important;
        border-radius: 999px !important;
        font-size: 1.2rem !important;
        padding: 0 !important;
    }
    .stButton > button:hover {
        background: #f3f4f6 !important;
    }

    /* Uploader compact : on enlève un peu de gras */
    .upload-inline [data-testid="stFileUploadDropzone"] {
        padding: 0.4rem 0.8rem !important;
    }

    /* Badges fichiers */
    .file-pill {
        display: inline-flex;
        align-items: center;
        background: #eef2ff;
        color: #3730a3;
        border-radius: 999px;
        padding: 4px 10px;
        font-size: .8rem;
        margin: 4px 6px 0 0;
    }

    /* Barre de recherche fixée en bas */
    .search-bar-fixed {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 1px solid #e5e7eb;
        padding: 1rem 2rem;
        z-index: 999;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
    }

    .search-bar-content {
        max-width: 1200px;
        margin: 0 auto;
    }

    .block-container {
        padding-bottom: 150px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("### ⚙️ Paramètres")
    st.markdown("Réglez l’opération avant de lancer le formulaire.")
    st.markdown("---")
    st.markdown("📦 **TabExplorer** by ECE")

# ----------------- HEADER -----------------
st.markdown(
    '<div class="tabx-title-wrapper"><div class="tabx-title">TabExplorer v0.1</div></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="tabx-subtitle">La combinaison entre l’exploration de données et les modèles IA ✨</div>',
    unsafe_allow_html=True,
)
st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

# ----------------- LAYOUT -----------------
# Centrer le formulaire avec des colonnes vides
col_empty1, col_form, col_empty2 = st.columns([0.15, 0.7, 0.15])

# ===== FORMULAIRE =====
with col_form:
    st.markdown(
        '<div class="tabx-section-header"><span class="tabx-section-title">📝 Formulaire</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="tabx-helper">Ajoutez un nouveau document au stockage ou lancez une recherche.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="tabx-label">Type d\'opération</div>', unsafe_allow_html=True)
    op_mode = st.selectbox("", ["Insertion", "Recherche"], label_visibility="collapsed")

    if op_mode == "Recherche":
        precision = st.slider("Précision de la recherche", 0, 100, 80, key="precision")
        st.caption(
            f"Précision actuelle : **{precision}/100** – plus la valeur est élevée, plus la recherche est stricte."
        )

    # Espace pour la conversation
    st.markdown("<div style='height: 8rem;'></div>", unsafe_allow_html=True)

# -------- Barre de recherche fixée en bas --------
st.markdown('<div class="search-bar-fixed"><div class="search-bar-content">', unsafe_allow_html=True)

# Initialiser les variables
files = st.session_state.insert_files if op_mode == "Insertion" else st.session_state.search_files
send_clicked = False
text = ""

# Barre façon ChatGPT : + | input | ➤
c_plus, c_input, c_send = st.columns([0.07, 0.86, 0.07])

# 1) Bouton + simple (pas de caret)
with c_plus:
     if st.button("\u2795\ufe0e", key="plus_button"):
        st.session_state.show_uploader = not st.session_state.show_uploader

# 2) Champ texte
with c_input:
    placeholder = (
        "Décrivez le document à insérer ou ajoutez un message…"
        if op_mode == "Insertion"
        else "Posez une question sur vos données…"
    )
    text = st.text_input(
        "",
        placeholder=placeholder,
        label_visibility="collapsed",
        key=f"text_{op_mode}",
    )

# 3) Bouton flèche
with c_send:
    send_clicked = st.button("➤", key=f"send_{op_mode}")

# Uploader affiché sous la barre si on clique sur +
if st.session_state.show_uploader:
    st.markdown('<div class="upload-inline">', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Ajouter des fichiers",
        type=["txt", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key=f"uploader_{op_mode}",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Synchroniser le session_state avec l'état actuel de l'uploader
    if uploaded:
        if op_mode == "Insertion":
            st.session_state.insert_files = list(uploaded)
        else:
            st.session_state.search_files = list(uploaded)
    else:
        # Si l'utilisateur a supprimé tous les fichiers de l'uploader,
        # on vide aussi la liste en mémoire
        if op_mode == "Insertion":
            st.session_state.insert_files = []
        else:
            st.session_state.search_files = []

    files = st.session_state.insert_files if op_mode == "Insertion" else st.session_state.search_files

# Affichage des fichiers
if files:
    st.markdown("**Fichiers ajoutés :**")
    for f in files:
        st.markdown(f"<span class='file-pill'>{f.name}</span>", unsafe_allow_html=True)

# Envoi
if send_clicked:
    if not text.strip() and not files:
        st.warning("Ajoutez un texte ou au moins un fichier avant d'envoyer.")
    else:
        if op_mode == "Insertion":
            st.success(
                f"Insertion envoyée avec texte « {text or '(vide)'} » "
                f"et {len(files)} fichier(s) attaché(s)."
            )
        else:
            st.success(
                f"Recherche envoyée : « {text or '(vide)'} », "
                f"précision {precision}/100, "
                f"{len(files)} fichier(s) attaché(s)."
            )

st.markdown('</div></div>', unsafe_allow_html=True)
