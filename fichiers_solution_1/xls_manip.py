#!.venv/bin/python3
import pandas as pd
from langchain_openai import ChatOpenAI

def pretraitement_xls(fichier_cible):
    inter1 = pd.read_excel(fichier_cible)
    return inter1

def communication_xls(fichier_cible,message):
    try :
        inter = pretraitement_xls(fichier_cible)
        llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)
        # Le prompt sera une chaine de caracteres formattee.
        prompt = (
                f"Apercu du XLS : \n"
                f"{inter}"
                f"Question : {message}"
                )
        reponse = llm.invoke(prompt)
        return reponse.content
    except Exception as e:
        return e

if __name__ == "__main__":
    print("xls_manip.py > OK !")
