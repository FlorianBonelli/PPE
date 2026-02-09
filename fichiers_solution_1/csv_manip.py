#!/usr/bin/python3
import os
import pandas as pd
from langchain_openai import ChatOpenAI

# Fonction pour prétraiter un fichier csv et donner
# un preview à l'application Streamlit...
def pretraitement_csv(fichier_csv_cible):
    # Pandas lit le fichier...
    try:
        dt = pd.read_csv(fichier_csv_cible)
        return dt
    except Exception as e:
        return e

# Fonction pour communiquer avec l'API OpenAI
# en utilisant un fichier CSV présent dans le serveur.
# IN : fichier_cible_csv -> chemin du fichier csv.
# IN : message -> la demande du client dans le formulaire.
# OUT : reponse.content -> la réponse de l'API.
def communication_csv(dt,message):
    try :
        llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)
        # Le prompt sera une chaine de caracteres formattee.
        prompt = (
                f"Apercu du CSV : \n"
                f"{dt}"
                f"Question : {message}"
                )
        reponse = llm.invoke(prompt)
        return reponse.content
    except Exception as e:
        return e

if __name__ == "__main__":
    print(os.getcwd())
    print("csv_manip : OK")
