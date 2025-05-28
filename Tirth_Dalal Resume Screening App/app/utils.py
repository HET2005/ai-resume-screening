import os

def allowed_file(filename):
    allowed_extensions = {'pdf', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()
