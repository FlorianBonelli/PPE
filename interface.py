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

# Thème moderne ChatGPT-like
THEME = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f7f7f7;
        --bg-tertiary: #ececf1;
        --accent-blue: #10a37f;
        --accent-blue-light: #19c37d;
        --text-primary: #0d0d0d;
        --text-secondary: #565869;
        --border: #d1d5db;
        --message-user: #10a37f;
        --message-assistant: #f7f7f7;
    }
    
    html, body {
        background-color: var(--bg-primary);
    }
    
    .stApp {
        background-color: var(--bg-primary);
    }
    
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }
    
    /* Header */
    .chatgpt-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: var(--bg-primary);
        border-bottom: 1px solid var(--border);
        padding: 1rem 2rem;
        z-index: 100;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .header-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .header-stats {
        display: flex;
        gap: 2rem;
        font-size: 0.9rem;
        color: var(--text-secondary);
    }
    
    .stat-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Main content area */
    .main-content {
        margin-top: 70px;
        margin-bottom: 100px;
        padding: 2rem;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
        min-height: calc(100vh - 170px);
    }
    
    /* Empty state */
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 400px;
        text-align: center;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .empty-state-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .empty-state-subtitle {
        font-size: 1rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
    }
    
    .example-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .example-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 0.75rem;
        padding: 1rem;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
    }
    
    .example-card:hover {
        background: var(--bg-tertiary);
        border-color: var(--accent-blue);
    }
    
    .example-card-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    .example-card-desc {
        font-size: 0.85rem;
        color: var(--text-secondary);
    }
    
    /* Messages */
    .message-container {
        margin-bottom: 1.5rem;
        display: flex;
        gap: 1rem;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .message-user {
        justify-content: flex-end;
    }
    
    .message-content {
        max-width: 70%;
        padding: 0.75rem 1rem;
        border-radius: 0.75rem;
        line-height: 1.5;
        word-wrap: break-word;
    }
    
    .message-user .message-content {
        background: var(--message-user);
        color: white;
        border-radius: 0.75rem 0.75rem 0 0.75rem;
    }
    
    .message-assistant .message-content {
        background: var(--message-assistant);
        color: var(--text-primary);
        border: 1px solid var(--border);
        border-radius: 0.75rem 0.75rem 0.75rem 0;
    }
    
    /* Input area */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, var(--bg-primary), rgba(255, 255, 255, 0.8));
        padding: 1.5rem 2rem;
        z-index: 99;
        border-top: 1px solid var(--border);
    }
    
    .input-wrapper {
        max-width: 900px;
        margin: 0 auto;
    }
    
    .search-bar {
        display: flex;
        gap: 0.5rem;
        align-items: flex-end;
    }
    
    .search-input-wrapper {
        flex: 1;
        display: flex;
        align-items: center;
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 0.75rem;
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
    }
    
    .search-input-wrapper:focus-within {
        border-color: var(--accent-blue);
        box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.1);
    }
    
    div[data-testid="stTextInput"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    div[data-testid="stTextInput"] input {
        background: transparent !important;
        border: none !important;
        outline: none !important;
        font-size: 1rem;
        color: var(--text-primary);
        padding: 0 !important;
        width: 100%;
    }
    
    div[data-testid="stTextInput"] input::placeholder {
        color: var(--text-secondary);
    }
    
    .action-buttons {
        display: flex;
        gap: 0.5rem;
    }
    
    .icon-btn {
        background: transparent;
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        padding: 0.5rem;
        cursor: pointer;
        font-size: 1.2rem;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
    }
    
    .icon-btn:hover {
        background: var(--bg-secondary);
        border-color: var(--accent-blue);
    }
    
    .send-btn {
        background: var(--accent-blue);
        border: none;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .send-btn:hover {
        background: var(--accent-blue-light);
    }
    
    .send-btn:disabled {
        background: var(--border);
        cursor: not-allowed;
    }
    
    /* Panels */
    .panel {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 0.75rem;
        padding: 1rem;
        margin-top: 0.5rem;
    }
    
    .panel-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* File uploader */
    div[data-testid="stFileUploader"] {
        background: transparent !important;
    }
    
    div[data-testid="stFileUploader"] section {
        border: 1px dashed var(--border) !important;
        border-radius: 0.75rem !important;
        padding: 1rem !important;
        background: var(--bg-secondary) !important;
    }
    
    /* Slider */
    div[data-testid="stSlider"] {
        padding: 0.5rem 0;
    }
    
    /* Buttons */
    .stButton button {
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: 1px solid var(--border);
        background: var(--bg-secondary);
        color: var(--text-primary);
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        background: var(--bg-tertiary);
        border-color: var(--accent-blue);
    }
    
    .mode-buttons {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .mode-btn {
        flex: 1;
        padding: 0.75rem;
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        background: var(--bg-secondary);
        cursor: pointer;
        font-weight: 600;
        transition: all 0.2s ease;
        text-align: center;
    }
    
    .mode-btn.active {
        background: var(--accent-blue);
        color: white;
        border-color: var(--accent-blue);
    }
    
    .mode-btn:hover {
        border-color: var(--accent-blue);
    }
</style>
"""

st.markdown(THEME, unsafe_allow_html=True)

# Initialisation
if "mode" not in st.session_state:
    st.session_state.mode = "recherche"
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

# Header
last_file = st.session_state.uploaded_files[-1].name if st.session_state.uploaded_files else "Aucun"
st.markdown(f"""
<div class="chatgpt-header">
    <div class="header-title">🔍 TabExplorer</div>
    <div class="header-stats">
        <div class="stat-item">📁 {len(st.session_state.uploaded_files)} fichiers</div>
        <div class="stat-item">📊 Mode: {st.session_state.mode.capitalize()}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content area
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

# Display messages or empty state
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🔍</div>
        <div class="empty-state-title">Bienvenue sur TabExplorer</div>
        <div class="empty-state-subtitle">Explorez vos données avec l'intelligence artificielle</div>
        <div class="example-grid">
            <div class="example-card">
                <div class="example-card-title">📊 Analyser</div>
                <div class="example-card-desc">Analysez vos données en profondeur</div>
            </div>
            <div class="example-card">
                <div class="example-card-title">🔎 Rechercher</div>
                <div class="example-card-desc">Trouvez exactement ce que vous cherchez</div>
            </div>
            <div class="example-card">
                <div class="example-card-title">📈 Visualiser</div>
                <div class="example-card-desc">Découvrez des insights visuels</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Display messages
    for msg in st.session_state.messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        
        if role == "user":
            st.markdown(f"""
            <div class="message-container message-user">
                <div class="message-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-container">
                <div class="message-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Input area (fixed at bottom)
st.markdown("""
<div class="input-container">
    <div class="input-wrapper">
        <div class="search-bar">
            <div class="search-input-wrapper">
""", unsafe_allow_html=True)

# Input field
user_input = st.text_input(
    "Message",
    placeholder="Posez une question ou décrivez ce que vous cherchez...",
    key="user_input",
    label_visibility="collapsed",
)

st.markdown("""
            </div>
            <div class="action-buttons">
""", unsafe_allow_html=True)

# Action buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("📁", key="toggle_upload", help="Ajouter un fichier", use_container_width=True):
        st.session_state.show_upload_panel = not st.session_state.show_upload_panel

with col2:
    if st.button("⚙️", key="toggle_precision", help="Précision", use_container_width=True):
        st.session_state.show_precision_panel = not st.session_state.show_precision_panel

with col3:
    if st.button("📤", key="send_message", help="Envoyer", use_container_width=True):
        if user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.user_input = ""
            st.rerun()

st.markdown("""
            </div>
        </div>
""", unsafe_allow_html=True)

# Upload panel
if st.session_state.show_upload_panel:
    st.markdown("""
    <div class="panel">
        <div class="panel-title">📁 Ajouter des fichiers</div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Glissez & déposez vos fichiers",
        type=["jpeg", "jpg", "png", "pdf", "txt", "csv", "xlsx"],
        label_visibility="collapsed",
        key="file_uploader",
    )
    if uploaded_file and uploaded_file not in st.session_state.uploaded_files:
        st.session_state.uploaded_files.append(uploaded_file)
        st.rerun()

# Precision panel
if st.session_state.show_precision_panel:
    st.markdown("""
    <div class="panel">
        <div class="panel-title">⚙️ Réglage de précision</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.precision = st.slider(
        "Précision",
        30,
        100,
        st.session_state.precision,
        1,
        key="precision_slider",
        label_visibility="collapsed",
    )
    st.markdown(f"<div style='color: var(--text-secondary); font-size: 0.9rem;'>Précision: {st.session_state.precision}%</div>", unsafe_allow_html=True)

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)
