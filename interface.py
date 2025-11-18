# import ia_manip 
import streamlit as st

try:
    import ia_manip  # type: ignore
except ImportError:  # pragma: no cover
    ia_manip = None  # type: ignore

DARK_THEME = {
    "page_bg": "#0f172a",
    "text": "#f4f7ff",
    "muted": "#c7cde2",
    "card_bg": "#131c2f",
    "sidebar_bg": "#11182a",
    "input_bg": "#1f2a44",
    "accent": "#7ab8ff",
    "divider": "#1f2a44",
    "card_shadow": "0 20px 40px rgba(0, 0, 0, 0.6)",
    "chat_wrapper_bg": "#0b1220",
    "spinner_track": "#1f2a44"
}


def appliquer_theme(theme):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {theme["page_bg"]} !important;
            color: {theme["text"]} !important;
        }}
        body {{
            background-color: {theme["page_bg"]} !important;
        }}
        div[data-testid="stSidebar"] {{
            background-color: {theme["sidebar_bg"]} !important;
            color: {theme["text"]} !important;
        }}
        div[data-testid="stSidebar"] * {{
            color: {theme["text"]} !important;
        }}
        hr {{
            border-color: {theme["divider"]} !important;
        }}
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4,
        .stMarkdown p, .stMarkdown span {{
            color: {theme["text"]};
        }}
        .stCaption, .caption {{
            color: {theme["muted"]} !important;
        }}
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {{
            background-color: {theme["input_bg"]} !important;
            color: {theme["text"]} !important;
        }}
        .stButton button {{
            background-color: {theme["accent"]} !important;
            color: #fff !important;
            border-radius: 8px;
            border: none;
        }}
        .chat-wrapper {{
            background-color: {theme["chat_wrapper_bg"]};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def afficher_header(theme):
    st.markdown(
        f"""
        <h1 style='text-align: center; color: {theme["accent"]};'>
            TabExplorer v0.1
        </h1>
        <p style='text-align: center; font-size:18px; color: {theme["muted"]};'>
            La combinaison entre l’exploration de données et les modèles IA ✨
        </p>
        <hr style="border: 1px solid {theme["divider"]};"/>
        """,
        unsafe_allow_html=True
    )


def afficher_interface_principale():
    # --- MENU LATERAL ---
    st.sidebar.title("⚙️ Paramètres")
    type_operation = st.sidebar.selectbox(
        "Type d'opération",
        ["Insertion", "Requête"],
        index=0
    )

    st.sidebar.markdown("---")
    st.sidebar.write("📦 **TabExplorer** by Florian")

    # --- LAYOUT ---
    colonne1, colonne2 = st.columns([1, 1])

    # --- COLONNE GAUCHE (formulaires) ---
    with colonne1:
        st.subheader("📝 Formulaire")

        if type_operation == "Insertion":
            with st.form("insertion", clear_on_submit=False):
                st.write("Ajoutez un nouveau document au stockage")

                fichier_cible = st.file_uploader(
                    label="Fichier à insérer",
                    type=["jpeg", "png", "pdf", "txt"]
                )

                soumission = st.form_submit_button("📤 Envoyer")

                if soumission:
                    if fichier_cible:
                        if ia_manip is None:
                            st.error("Module ia_manip introuvable. Veuillez l'ajouter.")
                        elif fichier_cible.type == "image/jpeg":
                            ia_manip.traitement_JPEG(fichier_cible)  # type: ignore[attr-defined]
                            st.success("Image JPEG traitée avec succès ✔️")

                        elif fichier_cible.type == "text/plain":
                            ia_manip.traitement_TXT(fichier_cible)  # type: ignore[attr-defined]
                            st.success("Fichier TXT traité avec succès ✔️")
                    else:
                        st.error("❌ Aucun fichier fourni")

        elif type_operation == "Requête":
            with st.form("recherche", clear_on_submit=False):
                st.write("Recherchez un document similaire")

                fichier_cible = st.file_uploader(
                    label="Modèle recherché",
                    type=["jpeg", "png", "pdf", "txt"]
                )

                precision = st.slider("Précision", 30, 90, 50, 1)
                soumission = st.form_submit_button("🔍 Rechercher")

                if soumission:
                    if ia_manip is None:
                        st.error("Module ia_manip introuvable. Veuillez l'ajouter.")
                    else:
                        st.info("Fonction de recherche à compléter…")

    # --- COLONNE DROITE (résultats) ---
    with colonne2:
        st.subheader("📊 Données générées")
        zone_de_texte_intermediaire = st.empty()
        zone_de_texte_intermediaire.text("Aucune donnée pour le moment.")
        st.caption("Simulez une génération pour accéder au chatbot.")

        st.markdown("---")
        if st.button("🤖 Tester le chatbot", use_container_width=True):
            st.session_state["mode"] = "chatbot"


def afficher_chatbot(theme):
    st.sidebar.title("🤖 Assistant TabExplorer")
    st.sidebar.write("Espace conversationnel en cours de conception.")
    st.sidebar.markdown("---")
    if st.sidebar.button("⬅️ Retour à TabExplorer"):
        st.session_state["mode"] = "exploration"

    st.markdown(
        f"""
        <style>
        .chat-wrapper {{
            background-color: {theme["chat_wrapper_bg"]};
            padding: 60px 40px;
            border-radius: 12px;
        }}
        .chat-card {{
            max-width: 520px;
            margin: 0 auto;
            background: {theme["card_bg"]};
            padding: 48px 32px;
            border-radius: 16px;
            box-shadow: {theme["card_shadow"]};
            text-align: center;
        }}
        .chat-card h2 {{
            font-size: 28px;
            margin-bottom: 12px;
            color: {theme["text"]};
        }}
        .chat-card p {{
            color: {theme["muted"]};
            font-size: 16px;
            margin-bottom: 24px;
        }}
        .chat-spinner {{
            width: 46px;
            height: 46px;
            margin: 0 auto;
            border: 4px solid {theme["spinner_track"]};
            border-top-color: {theme["accent"]};
            border-radius: 50%;
            animation: rotation 1s linear infinite;
        }}
        @keyframes rotation {{
            to {{ transform: rotate(360deg); }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    header_left, header_right = st.columns([3, 1])
    with header_left:
        st.subheader("Assistant documentaire")
        st.caption("Pose une question sur tes recherches TabExplorer.")
    with header_right:
        st.button("Nouvelle conversation", use_container_width=True)

    st.markdown(
        f"""
        <div class="chat-wrapper">
            <div class="chat-card">
                <h2>Bienvenue 👋</h2>
                <p>
                    Décris ta question sur les documents indexés et je préparerai
                    une réponse sourcée et alignée sur TabExplorer.
                </p>
                <div class="chat-spinner"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Envoyer un message")
    saisie = st.text_input(
        "Pose ta question…",
        placeholder="Ex. Résume les tendances de mes factures 2024",
        label_visibility="collapsed"
    )
    st.button("Envoyer (à venir)", disabled=True)

    if saisie:
        st.info("Le moteur de réponse sera branché prochainement.")


def main():
    if "mode" not in st.session_state:
        st.session_state["mode"] = "exploration"

    # --- CONFIG PAGE ---
    st.set_page_config(
        page_title="TabExplorer v0.1",
        page_icon="📁",
        layout="wide"
    )

    theme = DARK_THEME
    appliquer_theme(theme)

    # --- HEADER PRINCIPAL ---
    afficher_header(theme)

    if st.session_state["mode"] == "chatbot":
        afficher_chatbot(theme)
    else:
        afficher_interface_principale()


if __name__ == "__main__":
    main()
