from google.adk.agents import Agent
from google.adk.tools import google_search


import os
import sqlite3
from fpdf import FPDF
from datetime import datetime
import unicodedata

# Step 1: Create a function to generate and save PDF
def save_visaprocess_to_pdf_and_db(text_content_1 : str)-> dict:
    
    def clean(text_content_1): 
        return unicodedata.normalize("NFKD", text_content_1).encode("latin-1", "ignore").decode("latin-1")

    filename="visa_process.pdf"
    db_name="pdf_store2.db"
    # Create folder if it doesn't exist
    output_folder = "pdfs2"
    os.makedirs(output_folder, exist_ok=True)
    pdf_path = os.path.join(output_folder, filename)

    # Step 2: Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Split lines to avoid overflow
    for line in text_content_1.split('\n'):
        pdf.multi_cell(0, 10, clean(line))
    
    pdf.output(pdf_path)

    # Step 3: Store metadata into SQLite DB
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pdf_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            path TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL
        )
    ''')

    # Insert record
    cursor.execute('''
        INSERT INTO pdf_files (filename, path, created_at)
        VALUES (?, ?, ?)
    ''', (filename, pdf_path, datetime.now()))

    conn.commit()
    conn.close()

    return {
        "action": "save_visaprocess_to_pdf_and_db",
        "message": "save pdf",
    }




pdf_visa= Agent(
    name="pdf_visa",
    model="gemini-2.0-flash-001",
    description="visa process steps",
    instruction="""
        You are an agent that stores text content to a pdf in the db.
        you need to store the text in state key 'visa_process_key'
        use save_visaprocess_to_pdf_and_db for saving this to pdf and storing to db
        
        
        Delegate back to root_agent after output generated.
    """,
    tools=[
        save_visaprocess_to_pdf_and_db
    ]

)