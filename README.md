
# 🧠 English Compliance API  
_A Python AI Project for Grammar & Guideline Validation_

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)
![spaCy](https://img.shields.io/badge/NLP-spaCy%20%2B%20LanguageTool-orange)
![Tests](https://img.shields.io/badge/Tests-Pytest-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📘 Project Overview
**English Compliance API** is an AI-powered FastAPI application that analyzes uploaded documents (PDF or Word) and evaluates them against English writing guidelines — grammar, sentence structure, clarity, and readability.  
It also provides an option to **auto-rewrite** documents to make them compliant.

This project was developed as part of the **AI Python Developer Assessment**.

---

## ⚙️ Features
✅ Upload and analyze **Word or PDF** documents  
✅ Detect grammar, readability, and passive voice issues  
✅ Get a detailed compliance report  
✅ AI-powered rewriting of non-compliant sections  
✅ Download corrected files  
✅ Fully tested with Pytest  
✅ Docker-ready for deployment  

## 🧩 Tech Stack
- **FastAPI** — backend framework  
- **spaCy** — NLP for sentence parsing  
- **LanguageTool** — grammar and style checker  
- **textstat** — readability scoring  
- **Python-docx / PyMuPDF** — text extraction  
- **OpenAI GPT (optional)** — advanced rewriting  

---

## 🧠 Project Structure
```

english-compliance-api/
│
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   ├── routers/analyze.py      # Upload, analyze, rewrite, download
│   ├── services/
│   │   ├── extract.py          # PDF/DOCX text extraction
│   │   ├── checkers.py         # Grammar, readability, clarity checks
│   │   └── rewrite.py          # AI rewrite logic
│   ├── models/schemas.py       # Pydantic models
│
├── tests/
│   └── test_api.py             # Pytest suite (health + endpoints)
│
├── sample_docs/sample.docx     # Example document
├── requirements.txt
└── README.md

````

---

## 🚀 Setup & Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/pkumar457/english-compliance-api.git
cd english-compliance-api
````

### 2️⃣ Create & activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate    # on Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4️⃣ Run the API

```bash
uvicorn app.main:app --reload
```

Open browser → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Running Tests

```bash
pytest -v
```

✅ Expected:

```
3 passed in 7s
```

---

## 🐳 Run via Docker

```bash
docker build -t english-compliance-api .
docker run -p 8000:8000 english-compliance-api
```

---

## 📂 Example Endpoints

| Method | Endpoint                  | Description                            |
| ------ | ------------------------- | -------------------------------------- |
| `POST` | `/v1/analyze`             | Upload DOCX/PDF and get grammar report |
| `POST` | `/v1/rewrite`             | Auto-rewrite document to fix issues    |
| `GET`  | `/v1/download/{filename}` | Download rewritten DOCX file           |
| `GET`  | `/healthz`                | Health check                           |

---

## 🧾 Example Output

```json
{
  "report": {
    "ok": false,
    "issues": [
      {"type": "Grammar", "message": "Use 'was' instead of 'were'"},
      {"type": "Readability", "message": "Sentence too long"}
    ],
    "metrics": {
      "flesch_score": 67.3,
      "passive_sentences": 2
    }
  },
  "document_id": "3df2a1c9-XXXX"
}
```

---

### 🧩 How to Add This
1. In your GitHub repo page → click **“Add file” → “Create new file”**
2. Name it:  
```

README.md

```
3. Paste the above content.
4. Scroll down → click **“Commit changes”**
