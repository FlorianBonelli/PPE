import streamlit as st
from datetime import datetime
import os

# ==========================================
# VERSION SIMPLIFIÉE POUR TESTS D'ERGONOMIE
# ==========================================
# Cette version commente tous les imports de modules externes
# et crée des fonctions factices pour permettre de tester l'interface

def file_uploader_csv_callback():
    print("+++ file_uploader_csv_callback +++")

# Initialisation des infos de la sessions.
if 'mode' not in st.session_state:
    st.session_state.mode = "None"
if 'message' not in st.session_state:
    st.session_state.message = "Aucun message"
if 'type_reponse' not in st.session_state:
    st.session_state.type_reponse = None
if 'texte_entree' not in st.session_state:
    st.session_state.texte_entree = None
if 'resultat' not in st.session_state:
    st.session_state.resultat = None
if 'csv_in' not in st.session_state:
    st.session_state.csv_in = None

# Configuration de la page
st.set_page_config(
    page_title="TabExplorer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("TabExplorer v0.5 - Mode Ergonomie")
st.subheader("Explorateur de données tabulaires avec LLM",divider="red")

st.subheader("MODE : {}".format(st.session_state.mode))

# La sélection du mode d'opération.
# Le mode est selectionnée en appuyany sur un des quatres boutons.
interaction_zone = st.container()
with interaction_zone:
    c1, c2, c3, c4 = st.columns([1,1,1,1])
    with c1:
        if st.button("Requete CSV", key="btn_CSV", use_container_width=True):
            st.session_state.mode  = "csv"
            st.rerun()
    with c2:
        if st.button("Requete SQL", key="btn_SQL", use_container_width=True):
            st.session_state.mode  = "sql"
            st.rerun()
    with c3:
        if st.button("Requete DOC", key="btn_PDF", use_container_width=True):
            st.session_state.mode  = "pdf"
            st.rerun()
    with c4:
        if st.button("Requete XLS", key="btn_XLS", use_container_width=True):
            st.session_state.mode  = "xls"
            st.rerun()



# La partie de l'interface avec les petits boutons...

bottom_shell = st.container()
with bottom_shell:
    # Nous allons utiliser deux colonnes :
    # - Une colonne pour les formulaires.
    # - Une colonne pour les réponses/résultats.
    colonne_formulaire, colonne_resultat = st.columns([1,1])
    # La colonne pour les formulaires.
    with colonne_formulaire:
        match st.session_state.mode:

            case "csv":
                fichier_cible = st.file_uploader(label="Importez votre fichier CSV",type="csv")
                requete = st.text_area(label="Votre requête :",key="TEXT_AREA1")
                bouton = st.button(label="Envoyer",key="BUTTON1")
                info1 = st.empty()
                preview = st.empty()
                if fichier_cible is not None:
                    # Mode démo : afficher les premières lignes
                    import pandas as pd
                    try:
                        df = pd.read_csv(fichier_cible)
                        preview.dataframe(df.head())
                        info1.success(f"✅ Fichier chargé : {fichier_cible.name}")
                    except Exception as e:
                        preview.error(f"Erreur de lecture : {e}")
                else:
                    info1.write("Aucun fichier selectionné")
                    preview.write("???")

                if bouton:
                    if fichier_cible is not None and requete:
                        # Réponse factice pour tester l'ergonomie
                        st.session_state.resultat = f"🤖 Réponse simulée pour : '{requete}'\n\nCeci est une réponse de démonstration. L'IA analyserait normalement votre fichier CSV et répondrait à votre question."
                        st.session_state.type_reponse = "information"
                    else:
                        st.session_state.resultat = "⚠️ Veuillez charger un fichier et poser une question."
                        st.session_state.type_reponse = "information"
    
            case "sql":
                # Liste factice de tables
                liste_des_tables = ["employees", "departments", "salaries", "customers"]
                choix_table = st.selectbox("Table(s) disponible(s) :",liste_des_tables)
                requete = st.text_area("Votre demande :")
                bouton = st.button("Envoyer")
                preview = st.empty()
                if choix_table:
                    # Aperçu factice
                    preview.info(f"📊 Aperçu de la table '{choix_table}' (données simulées)")
                    import pandas as pd
                    df_demo = pd.DataFrame({
                        'id': [1, 2, 3],
                        'nom': ['Alice', 'Bob', 'Charlie'],
                        'valeur': [100, 200, 300]
                    })
                    preview.dataframe(df_demo)
                if bouton and requete:
                    st.session_state.resultat = f"🤖 Réponse SQL simulée pour : '{requete}'\n\nL'IA analyserait normalement la base de données et répondrait à votre question."
                    st.session_state.type_reponse = "information"

            case "pdf":
                fichier_cible = st.file_uploader(label="Importez votre fichier PDF",type="pdf")
                requete = st.text_area(label="Votre requête :",key="TEXT_AREA1")
                bouton = st.button(label="Envoyer",key="BUTTON1")
                info1 = st.empty()
                preview = st.empty()
                if fichier_cible is not None:
                    info1.success(f"✅ PDF chargé : {fichier_cible.name}")
                    preview.info("📄 Aperçu du PDF non disponible en mode ergonomie")
                else:
                    info1.write("Aucun fichier selectionné")
                    preview.write("???")
                if bouton:
                    if fichier_cible is not None and requete:
                        st.session_state.resultat = f"🤖 Réponse PDF simulée pour : '{requete}'\n\nL'IA analyserait normalement le contenu du PDF et répondrait à votre question."
                        st.session_state.type_reponse = "information"

            case "xls":
                fichier_cible = st.file_uploader(label="Importez votre fichier XLS",type=["xls", "xlsx"])
                requete = st.text_area(label="Votre requête :",key="TEXT_AREA1")
                bouton = st.button(label="Envoyer",key="BUTTON1")
                info1 = st.empty()
                preview = st.empty()
                if fichier_cible is not None:
                    # Mode démo : afficher les premières lignes
                    import pandas as pd
                    try:
                        df = pd.read_excel(fichier_cible)
                        preview.dataframe(df.head())
                        info1.success(f"✅ Fichier Excel chargé : {fichier_cible.name}")
                    except Exception as e:
                        preview.error(f"Erreur de lecture : {e}")
                else:
                    info1.write("Aucun fichier selectionné")
                    preview.write("???")

                if bouton:
                    if fichier_cible is not None and requete:
                        st.session_state.resultat = f"🤖 Réponse Excel simulée pour : '{requete}'\n\nL'IA analyserait normalement votre fichier Excel et répondrait à votre question."
                        st.session_state.type_reponse = "information"


        
    with colonne_resultat:

        match st.session_state.type_reponse:

            case None:
                st.info("👈 Sélectionnez un mode et posez une question pour voir les résultats ici")
            
            case "information":
                st.write(st.session_state.resultat)



