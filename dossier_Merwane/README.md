# 📂 Système d'Extraction Documentaire - Merwane

On peut transformer n'importe quel fichier (PDF, Excel, Image) en texte pour l'envoyer dans la base de données MySQL.


## 📋 Guide des Fichiers (Qui fait quoi ?)

Voici l'explication de mes fichiers pour l'intégration dans la base commune :

1. **`analyzer.py`** : C'est le "cerveau". Il contient toutes les fonctions pour lire les fichiers (Excel avec Pandas, PDF avec OCR, etc.).
2. **`main.py`** : C'est le serveur (API). C'est lui qui reçoit le fichier, appelle l'analyseur, et fait le `INSERT INTO` dans la base de données.
3. *`connexion_mamp.py`** : Contient les réglages de connexion (Host, Port, User, Password). À modifier ici si les réglages de la base commune changent.
4. **`create_tables.py`** : Un petit script à lancer une seule fois pour créer la table `documents` avec les bonnes colonnes (nom, texte_extrait, etc.).
5. **`utils_pdf.py`** : Contient les fonctions spécifiques pour gérer les PDF difficiles ou scannés.


# Installation des dépendances

Avant de lancer, il faut installer ces bibliothèques sur ton ordinateur :

```bash
pip install fastapi uvicorn mysql-connector-python pandas openpyxl tabulate python-docx python-pptx pdfplumber pytesseract pdf2image Pillow