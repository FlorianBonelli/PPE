# analyzer.py
import os
import json
import csv
import docx
from PyPDF2 import PdfReader
import mimetypes
import zipfile
import tempfile

MAX_SIZE_BYTES = 10 * 1024 * 1024  


def detect_mime(file_path):
    mime, _ = mimetypes.guess_type(file_path)
    return mime or "application/octet-stream"


def parse_pdf(path):
    try:
        reader = PdfReader(path)
        pages = reader.pages
        text = "\n".join([p.extract_text() or "" for p in pages])
        return text, len(pages), None
    except:
        return None, None, None


def parse_txt(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        return "".join(lines), len(lines)
    except:
        return None, None


def parse_docx_file(path):
    try:
        doc = docx.Document(path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text, None
    except:
        return None, None


def parse_csv_file(path):
    try:
        rows = []
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)

        preview = "\n".join([";".join(r) for r in rows[:50]])
        metadata = {"columns": rows[0], "rows": len(rows)}
        return preview, len(rows), metadata
    except:
        return None, None, None


def parse_json_file(path):
    try:
        data = json.load(open(path, "r"))
        pretty = json.dumps(data, indent=2)[:50000]
        return pretty, {"type": str(type(data))}
    except:
        return None, None
    

def parse_pages(path):
    try:
        with zipfile.ZipFile(path, 'r') as z:
            file_list = z.namelist()
            print(f"Contenu du .pages: {file_list}")
            
            preview_files = ['Preview.pdf', 'preview.pdf', 'QuickLook/Preview.pdf']
            
            for preview_file in preview_files:
                if preview_file in file_list:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
                        with z.open(preview_file) as pdf_file:
                            temp_pdf.write(pdf_file.read())
                        temp_path = temp_pdf.name
                    
                    text, nb_pages, metadata = parse_pdf(temp_path)
                    os.unlink(temp_path)
                    
                    if metadata is None:
                        metadata = {}
                    metadata["source"] = "pages_preview"
                    metadata["preview_file"] = preview_file
                    
                    return text, nb_pages, metadata
            
            text_files = [f for f in file_list if f.endswith(('.xml', '.txt', '.rtf'))]
            if text_files:
                metadata = {"contenu": file_list, "text_files": text_files}
                return "Fichier .pages - contenu technique disponible", None, metadata
            
            return None, None, {"error": "Aucun contenu lisible", "contenu": file_list}
            
    except Exception as e:
        return None, None, {"error": f"Erreur .pages: {str(e)}"}


def analyze_file(path, filename):
    size = os.path.getsize(path)
    if size > MAX_SIZE_BYTES:
        return None, "too_large"

    ext = filename.split(".")[-1].lower()
    mime = detect_mime(path)

    text, nb_pages, nb_lines, metadata = None, None, None, None

    if ext == "pdf":
        text, nb_pages, metadata = parse_pdf(path)
    elif ext == "pages":
        text, nb_pages, metadata = parse_pages(path)
    elif ext in ("txt", "md"):
        text, nb_lines = parse_txt(path)
    elif ext == "docx":
        text, nb_pages = parse_docx_file(path)
    elif ext == "csv":
        text, nb_lines, metadata = parse_csv_file(path)
    elif ext == "json":
        text, metadata = parse_json_file(path)
    else:
        text = None

    status = "parsed_ok" if text is not None else "parse_error"

    return {
        "name": filename,
        "extension": ext,
        "mime_type": mime,
        "size_bytes": size,
        "text_content": text,
        "nb_pages": nb_pages,
        "nb_lines": nb_lines,
        "metadata": json.dumps(metadata) if metadata else None,
        "status": status
    }, None