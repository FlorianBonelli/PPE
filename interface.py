# import ia_manip 
import streamlit as st

def main():

    # --- CONFIG PAGE ---
    st.set_page_config(
        page_title="TabExplorer v0.1",
        page_icon="📁",
        layout="wide"
    )

    # --- HEADER PRINCIPAL ---
    st.markdown(
        """
        <h1 style='text-align: center; color: #4A90E2;'>
            TabExplorer v0.1
        </h1>
        <p style='text-align: center; font-size:18px; color: grey;'>
            La combinaison entre l’exploration de données et les modèles IA ✨
        </p>
        <hr style="border: 1px solid #EEE;"/>
        """,
        unsafe_allow_html=True
    )

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
                    type=["jpeg","png","pdf","txt"]
                )

                soumission = st.form_submit_button("📤 Envoyer")

                if soumission:
                    if fichier_cible:
                        if fichier_cible.type == "image/jpeg":
                            ia_manip.traitement_JPEG(fichier_cible)
                            st.success("Image JPEG traitée avec succès ✔️")

                        elif fichier_cible.type == "text/plain":
                            ia_manip.traitement_TXT(fichier_cible)
                            st.success("Fichier TXT traité avec succès ✔️")
                    else:
                        st.error("❌ Aucun fichier fourni")

        elif type_operation == "Requête":
            with st.form("recherche", clear_on_submit=False):
                st.write("Recherchez un document similaire")

                fichier_cible = st.file_uploader(
                    label="Modèle recherché",
                    type=["jpeg","png","pdf","txt"]
                )

                precision = st.slider("Précision", 30, 90, 50, 1)
                soumission = st.form_submit_button("🔍 Rechercher")

                if soumission:
                    st.info("Fonction de recherche à compléter…")

    # --- COLONNE DROITE (résultats) ---
    with colonne2:
        st.subheader("📊 Données générées")
        zone_de_texte_intermediaire = st.empty()
        zone_de_texte_intermediaire.text("Aucune donnée pour le moment.")


if __name__ == "__main__":
    main()
