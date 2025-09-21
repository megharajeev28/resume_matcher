import fitz  # PyMuPDF
from docx import Document
import re

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return ""

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    try:
        doc = Document(docx_path)
        text = [para.text for para in doc.paragraphs]
        return "\n".join(text)
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return ""

def get_text_from_file(file_path):
    """Determines file type and extracts text."""
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error extracting TXT: {e}")
            return ""
    else:
        print(f"Unsupported file type: {file_path}")
        return ""
