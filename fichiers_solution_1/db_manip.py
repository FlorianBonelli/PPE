#!/usr/bin/python3
import pg8000 # La librairie Python pour communiquer avec la BDD PostgreSQL...

def insertion_vecteur(vecteur_cible,chemin_fichier):
    # D'abord on se connecte à la BDD TEDB0.
    connexion = pg8000.dbapi.Connection(
            database="TEDB0",
            password="motdepassealanoix",
            user="tepsqluser0"
            )
    curseur = connexion.cursor()
    vecteur_conversion = str(vecteur_cible.numpy()[0])
    vecteur_conversion1 = vecteur_conversion.replace("\n","")
    vecteur_conversion2 = "[" + ",".join(vecteur_conversion1.strip("[]").split()) + "]"
    resultat = curseur.execute("INSERT INTO stockage1 VALUES ('{}','{}') ;".format(vecteur_conversion2,chemin_fichier))
    connexion.commit()
    # On ferme la connexion.
    connexion.close()
    return resultat

def recherche_vecteur(vecteur_de_recherche,niveau_de_precision):
    # D'abord on se connecte à la BDD TEDB0.
    connexion = pg8000.dbapi.Connection(
            database="TEDB0",
            password="motdepassealanoix",
            user="tepsqluser0"
            )
    curseur = connexion.cursor()
    vecteur_conversion = str(vecteur_de_recherche.numpy()[0])
    vecteur_conversion1 = vecteur_conversion.replace("\n","")
    vecteur_conversion2 = "[" + ",".join(vecteur_conversion1.strip("[]").split()) + "]"
    execution = curseur.execute("SELECT * FROM stockage1 ORDER BY vecteur <->'{}' LIMIT 5;".format(vecteur_conversion2))
    rows = curseur.fetchall()
    # On ferme la connexion.
    connexion.close()
    return rows 

   

