#!/usr/bin/python3
# Les librairies de bases / élémentaires.
import os
import io

# Les librairies pour le traitement des Images par le modèle CLIP de OpenAI.
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer, CLIPTextModel 
import torch
from PIL import Image

nom_modele = "openai/clip-vit-base-patch32"

# Chargement du modèle CLIP pour les images...
processeur_CLIP = CLIPProcessor.from_pretrained(nom_modele)
modele_CLIP = CLIPModel.from_pretrained(nom_modele)

# Chargement du modèle CLIP pour les textes...
tokenizer_CLIP = CLIPTokenizer.from_pretrained(nom_modele)
modele_CLIP_texte = CLIPTextModel.from_pretrained(nom_modele)

"""
********************************************************************************
Ce programme Python doit contenir toutes les fonctions liés de près ou de loin à
l'utilisation des LLMs. Notamment des fonctions qui convertissent/transforment
les informations données en entrée dans les formulaires de l'interface Streamlit.
********************************************************************************

Lien(s) utile(s):

OpenAI Python Software Development Kit (Pour communiquer avec les LLMs)
https://platform.openai.com/docs/api-reference/introduction?lang=python

¿¿¿ QUEL type de workflow pour QUEL type d'entrée ???

fichiers TXT : traitement direct + envoi au modele "text-embedding-3-small"
fichiers PDF : Extraction du texte ET des images en utilisant la librairie Py2PDF2
                    + envoi du texte extrait au modele "text-embedding-3-small"
                    + envoi des images extraits au modele "CLIP".
fichiers JPEF,PNG : Traitement des images + envoi au model "CLIP"

"""

def communication_texte_IA(texte_cible):
    with torch.no_grad():
        sortie = modele_CLIP_texte(**texte_cible)
        return sortie.pooler_output

def communication_image_IA(image_cible):
    with torch.no_grad():
        sortie = modele_CLIP(**image_cible)
        return sortie.image_embeds

def traitement_TXT(fichier_cible):
    intermediaire1 = io.StringIO(fichier_cible.getvalue().decode("utf-8"))
    lecture = intermediaire1.read()
    intermediaire2 = tokenizer_CLIP(lecture,return_tensors="pt")
    resultat = communication_texte_IA(intermediaire2)
    return resultat

def traitement_PDF(fichier_cible):
    pass

def traitement_JPEG(fichier_cible,insertion=False):

    url_fichier = "tabexplorer_stockage_fichiers/{}".format(fichier_cible.name)
    
    if insertion:
        # On essaye d'abord d'enregistrer l'image...
        try :
            fichier_cible.seek(0)
            image_sauvegarde = Image.open(fichier_cible)
            image_sauvegarde.save(url_fichier)
        except Exception as erreur:
            return erreur

    # Si l'image a été enregistrée avec succès, on le fait traiter auprès du modèle.
    with Image.open(fichier_cible) as intermediaire1 :
        intermediaire2 = processeur_CLIP( text="une image", images=intermediaire1 , return_tensors="pt" , padding=True )
        resultat = communication_image_IA(intermediaire2)
        return [resultat,url_fichier] 

def traitement_PNG(fichier_cible):
    pass


