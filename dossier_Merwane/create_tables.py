# create_tables.py
from connexion_mamp import get_db

def create_tables():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            extension VARCHAR(20),
            mime_type VARCHAR(100),
            size_bytes INT,
            text_content LONGTEXT,
            nb_pages INT,
            nb_lines INT,
            metadata JSON,
            status VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("Table 'documents' valide")


if __name__ == "__main__":
    create_tables()