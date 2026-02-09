import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import ia_manip
import db_manip
import pdf_manip
import langchain_manip
import csv_manip
import xls_manip
from datetime import datetime
import os

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

st.title("TabExplorer v0.5")
st.subheader("Explorateur de données tabulaires avec LLM",divider="red")

st.subheader("MODE : {}".format(st.session_state.mode))

# La sélection du mode d'opération.
# Le mode est selectionnée en appuyany sur un des quatres boutons.
interaction_zone = st.container()
with interaction_zone:
    c1, c2, c3, c4 = st.columns([1,1,1,1])
    with c1:
        if st.button("Requete CSV", key="btn_CSV", width="stretch"):
            st.session_state.mode  = "csv"
            st.rerun()
    with c2:
        if st.button("Requete SQL", key="btn_SQL", width="stretch"):
            st.session_state.mode  = "sql"
            st.rerun()
    with c3:
        if st.button("Requete DOC", key="btn_PDF", width="stretch"):
            st.session_state.mode  = "pdf"
            st.rerun()
    with c4:
        if st.button("Requete XLS", key="btn_XLS", width="stretch"):
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
                    fichier_cible.seek(0)
                    intermediaire1 = csv_manip.pretraitement_csv(fichier_cible)
                    preview.write(intermediaire1)
                else:
                    info1.write("Aucun fichier selectionné")
                    preview.write("???")

                if bouton:
                    if fichier_cible is not None:
                        fichier_cible.seek(0)
                        intermediaire1 = csv_manip.pretraitement_csv(fichier_cible)
                        out1 = csv_manip.communication_csv(intermediaire1,requete)
                        st.session_state.resultat = out1
                        st.session_state.type_reponse = "information"
    
            case "sql":
                liste_des_tables = langchain_manip.listing_tables_sql()
                choix_table = st.selectbox("Table(s) disponible(s) :",liste_des_tables)
                requete = st.text_area("Votre demande :")
                bouton = st.button("Envoyer")
                preview = st.empty()
                if choix_table:
                    preview.write(langchain_manip.preview_table(choix_table))
                if bouton:
                    out1 = langchain_manip.communication_langchain(requete)
                    st.session_state.resultat = out1
                    st.session_state.type_reponse = "information"

            case "pdf":
                fichier_cible = st.file_uploader(label="Importez votre fichier PDF",type="pdf")
                requete = st.text_area(label="Votre requête :",key="TEXT_AREA1")
                bouton = st.button(label="Envoyer",key="BUTTON1")
                info1 = st.empty()
                preview = st.empty()
                if fichier_cible is not None:
                    intermediaire1 = pdf_manip.preview_pdf(fichier_cible)
                    st.image(intermediaire1[0])
                else:
                    info1.write("Aucun fichier selectionné")
                    preview.write("???")
                if bouton:
                    if fichier_cible is not None:
                        out1 = pdf_manip.communication_pdf(fichier_cible,requete)
                        st.session_state.resultat = out1
                        st.session_state.type_reponse = "information"

            case "xls":
                fichier_cible = st.file_uploader(label="Importez votre fichier XLS",type="xls")
                requete = st.text_area(label="Votre requête :",key="TEXT_AREA1")
                bouton = st.button(label="Envoyer",key="BUTTON1")
                info1 = st.empty()
                preview = st.empty()
                if fichier_cible is not None:
                    fichier_cible.seek(0)
                    intermediaire1 = xls_manip.pretraitement_xls(fichier_cible)
                    preview.write(intermediaire1)
                else:
                    info1.write("Aucun fichier selectionné")
                    preview.write("???")

                if bouton:
                    if fichier_cible is not None:
                        fichier_cible.seek(0)
                        out1 = xls_manip.communication_xls(fichier_cible,requete)
                        st.session_state.resultat = out1
                        st.session_state.type_reponse = "information"


        
    with colonne_resultat:

        match st.session_state.type_reponse:

            case None:
                pass
            
            case "information":
                st.write(st.session_state.resultat)



