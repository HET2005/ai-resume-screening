<!-- @format -->

# ResuStreamPro

ResuStreamPro is an AI-powered resume screening web application built with Streamlit. It leverages state-of-the-art NLP models to automate and streamline the candidate shortlisting process for recruiters and HR professionals.

## Features

- **Upload Resumes:** Supports PDF, DOCX, and TXT files. Upload multiple resumes at once.
- **AI Model Selection:** Choose from several SentenceTransformer models for semantic matching.
- **Job Description Matching:** Paste a job description and instantly match it against uploaded resumes using cosine similarity of embeddings.
- **Threshold Filtering:** Set a similarity threshold to filter top candidates.
- **Dashboard:** View ranked candidates, inspect similarity scores, and see processed resume snippets.
- **Settings:** Adjust global settings, clear model cache, and manage advanced options.

## How It Works

1. **Upload resumes** via the Upload page. The app extracts and preprocesses text, then generates embeddings using the selected AI model.
2. **Paste a job description** on the Dashboard. The app computes its embedding and compares it to all uploaded resumes using cosine similarity.
3. **View results:** Candidates are ranked by similarity. Filter by threshold and inspect details for each candidate.

## Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **NLP Models:** [SentenceTransformers](https://www.sbert.net/)
- **Text Extraction:** PyPDF2, python-docx
- **Similarity:** Cosine similarity via SentenceTransformers utilities

## Installation

1. **Clone the repository:**
   ```
   git clone <your-repo-url>
   cd resume_screener_app
   ```
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```
   streamlit run app.py
   ```

## File Structure

- `app.py` — Main Streamlit app with UI and logic
- `utils.py` — Utility functions for model loading, text extraction, preprocessing, embeddings, and similarity
- `requirements.txt` — Python dependencies
- `data/` — (Optional) Folder for storing sample resumes

## Usage

- Use the sidebar to navigate between Home, Upload, Dashboard, and Settings.
- Upload resumes on the Upload page. Already-uploaded files are skipped.
- On the Dashboard, paste a job description and click "Match Candidates" to see ranked results.
- Adjust the similarity threshold in the sidebar or Settings page.
- Clear uploaded resumes or model cache as needed.

## Supported Models

- `all-MiniLM-L6-v2` (default)
- `paraphrase-MiniLM-L6-v2`
- `multi-qa-MiniLM-L6-cos-v1`

## Notes

- Maximum file size per resume: 200MB
- Only PDF, DOCX, and TXT formats are supported
- Model downloads may take time on first run

## License

This project is for educational and demonstration purposes. Please check individual package licenses for commercial use.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [SentenceTransformers](https://www.sbert.net/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [python-docx](https://python-docx.readthedocs.io/en/latest/)
