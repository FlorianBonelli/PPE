# utils_pdf.py
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
import cv2
import numpy as np

def preprocess_image_pour_ocr(pil_image):
    """
    Nettoie une image pour améliorer la lecture par Tesseract (OCR).
    Convertit en niveaux de gris et augmente le contraste.
    """
    try:
        img_np = np.array(pil_image)
        
        if img_np.shape[-1] == 4:
            img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)
            
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        

        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return Image.fromarray(thresh)
    except Exception as e:
        print(f"Warning: Echec du pré-traitement image ({e}), utilisation image brute.")
        return pil_image

def lire_image_directe(file_bytes):
    """
    Lit une image (JPG, PNG) avec nettoyage préalable.
    """
    try:
        image = Image.open(io.BytesIO(file_bytes))
        image_clean = preprocess_image_pour_ocr(image)
        text = pytesseract.image_to_string(image_clean, lang='fra+eng')
        return text, "OCR_IMAGE_OPTIMISE"
    except Exception as e:
        print(f"Erreur lecture image: {e}")
        return "", "ERREUR"

def lire_pdf_robuste(file_bytes):
    """
    Approche HYBRIDE et INTELLIGENTE :
    1. Parcourt le PDF page par page.
    2. Tente d'extraire les tableaux structurés.
    3. Tente d'extraire le texte natif.
    4. Si pas assez de texte -> Convertit la page en image -> Nettoie -> OCR.
    """
    full_content = []
    methodes = set()
    
    try:
        # On charge le PDF
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            total_pages = len(pdf.pages)

            images_pdf = None 

            for i, page in enumerate(pdf.pages):
                page_text_parts = []
                header = f"--- PAGE {i+1}/{total_pages} ---"
                
                tables = page.extract_tables()
                if tables:
                    page_text_parts.append("[TABLEAU DÉTECTÉ]")
                    for table in tables:
                        for row in table:
                            clean_row = [str(cell).replace("\n", " ") if cell else "" for cell in row]
                            page_text_parts.append(" | ".join(clean_row))
                    page_text_parts.append("[FIN TABLEAU]\n")
                
                text_natif = page.extract_text()

                if (not text_natif or len(text_natif.strip()) < 50) and not tables:
                    try:
                        if images_pdf is None:
                            images_pdf = convert_from_bytes(file_bytes)
                        
                        if i < len(images_pdf):
                            img_page = images_pdf[i]
                            img_clean = preprocess_image_pour_ocr(img_page)
                            text_ocr = pytesseract.image_to_string(img_clean, lang='fra+eng')
                            
                            page_text_parts.append(f"[OCR]:\n{text_ocr}")
                            methodes.add("OCR")
                    except Exception as e:
                        page_text_parts.append(f"[Erreur OCR]: {e}")
                else:
                    if text_natif:
                        page_text_parts.append(text_natif)
                    methodes.add("NATIVE")

                full_content.append(header + "\n" + "\n".join(page_text_parts))

        return "\n\n".join(full_content), f"HYBRIDE ({', '.join(methodes)})"

    except Exception as e:
        print(f"Erreur PDF globale: {e}")
        return "", "ERREUR_CRITIQUE"