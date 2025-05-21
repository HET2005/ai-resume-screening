# 📅 Internship Daily Report – AI-Powered Resume Screening System

**🎯 Project Title:** Resume Screening System using NLP and Semantic Similarity  
**🧠 Internship Domain:** Machine Learning / Natural Language Processing  
**✍️ Author:** Vishruti Parekh
**📅 Internship Period:** 12/05/2025 – [End Date]  

---

## ✅ Overview

The objective of this internship project is to build an **AI-powered Resume Ranking System** that automatically matches resumes to job descriptions using NLP techniques such as **TF-IDF**, **Word2Vec**, and **BERT-based embeddings**.  
This document outlines the **day-wise progress report** for the entire model-building process.

---

## 📌 Daily Log

### 📍 **Day 1: Dataset Identification and Exploration**

- Explored multiple public datasets for resumes (e.g., Kaggle’s Resume Dataset).
- Selected a labeled dataset containing fields like `Category` and `Resume`.
- Loaded the dataset using **Pandas** and conducted initial inspection.
- Verified dataset quality, checked for null values, and reviewed resume samples.

---

### 📍 **Day 2: Research on Resume Ranking and Similarity Models**

- Conducted a literature review on automated resume screening systems.
- Compared techniques: **TF-IDF**, **Word2Vec (GloVe)**, **BERT**.
- Identified **cosine similarity** as the core matching metric.
- Decided to benchmark multiple embeddings for accuracy comparison.

---

### 📍 **Day 3: Data Cleaning and Preprocessing**

- Created a `clean_text()` function using **spaCy** to:
  - Tokenize and lemmatize
  - Convert to lowercase
  - Remove punctuation and stopwords
- Applied cleaning to all resumes → stored in `Cleaned_Resume`.
- Ensured normalized text for vectorization.

---

### 📍 **Day 4: Text Extraction from PDF Resumes**

- Integrated `pdfminer.six` and `PyMuPDF (fitz)` for PDF parsing.
- Scripted batch PDF processing → extracted structured content.
- Manually verified parsed text vs. original PDFs for accuracy.
- Ensured formatting consistency with the preprocessed dataset.

---

### 📍 **Day 5: Updating and Structuring the Dataset**

- Merged extracted resumes with the original dataset.
- Created `final_resumes.csv` with:
  - `Resume`, `Cleaned_Resume`, `Category`, `Source`
- Removed duplicates, trimmed whitespaces, and handled encoding.

---

### 📍 **Day 6: Implementing TF-IDF and BERT-based Embeddings**

- **TF-IDF:**
  - Applied `TfidfVectorizer` (1000 features).
  - Transformed job descriptions and computed cosine similarity.

- **BERT:**
  - Used `all-MiniLM-L6-v2` via `sentence-transformers`.
  - Encoded resumes and job descriptions into semantic vectors.
  - Achieved high-ranking accuracy.

---

### 📍 **Day 7: Word2Vec Embeddings and Model Comparison**

- Loaded pre-trained **GloVe (100D)** via `gensim`.
- Created document-level vectors via averaged word embeddings.
- Compared cosine similarities across models.

#### 📊 **Model Comparison Table**

| **Model** | **Accuracy (Top-K Relevance)** | **Remarks**                       |
|----------|-------------------------------|----------------------------------|
| TF-IDF   | Medium (60–70%)               | Fast, lacks context              |
| Word2Vec | Medium-High (65–75%)          | Captures word semantics          |
| BERT     | High (80–90%)                 | Best contextual understanding    |

---

### 📍 **Day 8: Finalizing and Saving the Model**

- Finalized **BERT** for deployment due to superior performance.
- Saved the following:
  - Clean dataset: `final_resumes.csv`
  - Models: `tfidf_model.pkl`, `resume_embeddings.pkl`
  - Scripts: ranking logic and similarity functions
- Documented full pipeline:

```txt
PDF/Text Resume → Clean → Vectorize → Match with JD → Rank
```
