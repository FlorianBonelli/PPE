from pypdf import PdfReader
from PIL import Image
from pdf2image import convert_from_bytes
import io
from openai import OpenAI

client = OpenAI()

def preview_pdf(fichier_cible):
    imagus = convert_from_bytes(fichier_cible.read(),first_page=1,last_page=1)
    return imagus

def pretraitement_pdf(fichier_cible):
    lecteur = PdfReader(fichier_cible)
    texte = ""
    for page in lecteur.pages:
        texte += page.extract_text() + "\n"
    return texte

def communication_pdf(fichier_cible,question):
    texte_du_fichier = pretraitement_pdf(fichier_cible)
    chaine = f"Voici le contenu textuel d'un document : {texte_du_fichier} Question : {question}"
    reponse = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role":"user","content":chaine}])
    return reponse.choices[0].message.content


if __name__ == "__main__":
    question = "Quel sont les catégories d'handicap avec 5 participants ?"
    reponse1 = communication_pdf("sample2.pdf",question)
    print(reponse1)
