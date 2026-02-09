#!/usr/bin/python3
import ia_manip
import db_manip
import streamlit as str

def main():

    # Introduction rapide de la solution.
    str.title("TabExplorer v0.1")
    str.write("La combinaison entre la recherche de données et les langages de modèle !")

    # Définition des colonnes.
    # La colonne 1 est consacrée aux formulaires d'entrées.
    # La colonne 2 est dediée aux sorties.
    colonne1, colonne2 = str.columns([1,1],gap="medium")

    # Liste des résultats des requêtes...
    liste_resultat = []

    # Définition de la colonne 1
    with colonne1:

        # Le client choisit l'opération qu'il souhaite faire.
        type_operation = str.selectbox(label="Type d'opération",options=["Insertion","Requete"],index=0)

        match type_operation:

            # Formulaire en cas d'insertion
            case "Insertion":
                with str.form("insertion",clear_on_submit=False):
                    str.header("Ajouter un nouveau document")
                    fichier_cible = str.file_uploader(label="Modèle à insérer",type=["jpeg","png","pdf","txt"])
                    soumission = str.form_submit_button('Envoyer')
                    if soumission:
                        #print(fichier_cible)
                        if fichier_cible != None :
                            match fichier_cible.type:
                                case 'image/jpeg':
                                    out1 = ia_manip.traitement_JPEG(fichier_cible,True)
                                    res1 = db_manip.insertion_vecteur(out1[0],out1[1])
                                case 'text/plain':
                                    out1 = ia_manip.traitement_TXT(fichier_cible,True)
                                    res1 = db_manip.insertion_vecteur(out1)
                        else:
                            str.write("Le fichier d'entrée est manquant :(")

            # Formulaire en cas de requête
            case "Requete":
                with str.form("recherche",clear_on_submit=False):
                    str.header("Rechercher un document")
                    fichier_cible = str.file_uploader(label="Modèle recherché",type=["jpeg","png","pdf","txt"])
                    if fichier_cible:
                        str.write("Entrée :")
                        if fichier_cible != None :
                            match fichier_cible.type:
                                case 'image/jpeg':
                                    str.image(fichier_cible)
                    soumission = str.form_submit_button('Envoyer')
                    if soumission:
                        if fichier_cible != None :
                            match fichier_cible.type:
                                case 'image/jpeg':
                                    out1 = ia_manip.traitement_JPEG(fichier_cible,False)
                                    liste_resultat = db_manip.recherche_vecteur(out1[0],0)
                                case 'text/plain':
                                    out1 = ia_manip.traitement_TXT(fichier_cible)
                                    liste_resultat = db_manip.insertion_vecteur(out1[0],0)
                        else:
                            str.write("Le fichier d'entrée est manquant :(")

    # Définition de la colonne 2
    with colonne2:

        introduction1 = str.write("Résultat(s) :")

        for resultat in liste_resultat:
            str.image(resultat[1],width="stretch")



if __name__ == "__main__":
	main()
