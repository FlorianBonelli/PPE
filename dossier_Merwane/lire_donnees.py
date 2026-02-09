# # lire_donnees.py
# from connexion_mamp import connect_to_mamp

# def lire_infos():
#     conn = connect_to_mamp()
#     if conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM donnees_python")
#         resultats = cursor.fetchall()
        
#         print(" Données stockées dans la base:")
#         for ligne in resultats:
#             print(f"ID: {ligne[0]}, Nom: {ligne[1]}, Email: {ligne[2]}, Date: {ligne[3]}")
        
#         conn.close()

# lire_infos()