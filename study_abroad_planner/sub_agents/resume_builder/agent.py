from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

import os
import sqlite3
from fpdf import FPDF
from datetime import datetime

# Step 1: Create a function to generate and save PDF
def save_text_to_pdf_and_db(text_content : str)-> dict:
    filename="output.pdf"
    db_name="pdf_store.db"
    # Create folder if it doesn't exist
    output_folder = "pdfs"
    os.makedirs(output_folder, exist_ok=True)
    pdf_path = os.path.join(output_folder, filename)

    # Step 2: Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Split lines to avoid overflow
    for line in text_content.split('\n'):
        pdf.multi_cell(0, 10, line)
    
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
        "action": "save_text_to_pdf_and_db",
        "message": "save pdf",
    }


resume_builder= Agent(
    name="resume_builder",
    model="gemini-2.0-flash-001",
    description="Generates resume",
    instruction="""
        You are a text resume builder agent.
        Your job is to create a small text resume by asking the user necessary detailes required for a small resume with 3 basic information.
        Generate  a resume for the user using  the provided information and provide the output to user and also use save_text_to_pdf_and_db
        
        
        Delegate back to root_agent after output generated.
    """,
    tools=[
        save_text_to_pdf_and_db
    ]

)