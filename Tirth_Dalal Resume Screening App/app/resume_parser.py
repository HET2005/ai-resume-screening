import pdfminer.high_level
import docx2txt

print("resume_parser.py loaded")


def extract_text_from_pdf(file_path):
    try:
        return pdfminer.high_level.extract_text(file_path)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(file_path):
    try:
        return docx2txt.process(file_path)
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
        return ""     

def extract_resume_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Use PDF or DOCX.")