import mammoth
from pdfminer.high_level import extract_text

def parse_pdf(path):
    return extract_text(path)

def parse_docx(path):
    try:
        with open(path, "rb") as docx_file:
            result = mammoth.extract_raw_text(docx_file)
            return result.value.strip()
    except Exception as e:
        raise Exception(f"Mammoth DOCX read failed: {e}")

def extract_text_from_file(file_path):
    if file_path.lower().endswith(".pdf"):
        return parse_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        return parse_docx(file_path)
    else:
        raise ValueError(f"❌ Unsupported file format: {file_path}")
