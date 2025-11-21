# # stocker_donnees.py
# from connexion_mamp import connect_to_mamp

# def stocker_infos(nom, email):
#     conn = connect_to_mamp()
#     if conn:
#         cursor = conn.cursor()
        
#         # Insère les données
#         cursor.execute(
#             "INSERT INTO donnees_python (nom, email) VALUES (%s, %s)",
#             (nom, email)
#         )
#         conn.commit()
#         print(f"Données stockées: {nom}, {email}")
#         conn.close()

# # Exemple d'utilisation
# if __name__ == "__main__":
#     # Tes données à stocker
#     nom = "Pierre Dupont"
#     email = "pierre@email.com"
    
#     stocker_infos(nom, email)