# main.py
from fastapi import FastAPI, UploadFile, File
import os
import shutil
from datetime import datetime
from connexion_mamp import get_db
from analyzer import analyze_file

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename
    save_path = os.path.join(UPLOAD_DIR, filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result, error = analyze_file(save_path, filename)

    if error == "too_large":
        os.remove(save_path)
        return {"error": "Fichier trop lourd (> 10 Mo)"}

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO documents
        (name, extension, mime_type, size_bytes, text_content, nb_pages, nb_lines, metadata, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        result["name"],
        result["extension"],
        result["mime_type"],
        result["size_bytes"],
        result["text_content"],
        result["nb_pages"],
        result["nb_lines"],
        result["metadata"],
        result["status"],
    ))

    conn.commit()
    conn.close()

    return {"status": "ok", "file": filename}


@app.get("/documents/")
def list_docs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM documents")
    rows = cursor.fetchall()
    conn.close()
    return rows