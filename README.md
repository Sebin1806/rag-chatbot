# 🤖 Advanced RAG Chatbot for Technical Documentation

An advanced Retrieval-Augmented Generation (RAG) chatbot built with **FastAPI**, **React**, **ChromaDB**, **Sentence Transformers**, and **Large Language Models (LLMs)**.

The chatbot allows users to upload PDF documents and ask natural language questions. It retrieves the most relevant information using advanced retrieval techniques before generating accurate, context-aware answers.

---

# 📌 Features

## 📄 Document Processing

* Upload PDF documents
* Automatic PDF text extraction
* Intelligent text chunking
* Metadata generation
* Vector embedding creation
* ChromaDB vector storage

---

## 🔍 Advanced Retrieval Pipeline

This project includes several advanced RAG techniques:

* ✅ Dense Vector Search
* ✅ Multi-Query Retrieval
* ✅ Hybrid Search (Dense + BM25)
* ✅ Cross-Encoder Reranking
* ✅ Neighbor Retrieval
* ✅ Context Compression
* ✅ Streaming Responses

---

# 🏗️ Retrieval Architecture

```text
                   User Question
                         │
                         ▼
              Multi Query Generation
                         │
                         ▼
            Hybrid Search (Dense + BM25)
                         │
                         ▼
           Cross Encoder Reranker
                         │
                         ▼
              Neighbor Retrieval
                         │
                         ▼
             Context Compression
                         │
                         ▼
              Large Language Model
                         │
                         ▼
                  Final Response
```

---

# 🛠️ Tech Stack

## Backend

* Python
* FastAPI
* Uvicorn

## Frontend

* React
* Vite
* Tailwind CSS
* Axios

## AI / NLP

* Sentence Transformers
* Cross Encoder
* BM25 Ranking
* ChromaDB
* Hugging Face Models

---

# 📂 Project Structure

```
rag-chatbot/

│
├── backend/
│   ├── app/
│   ├── uploads/
│   ├── chroma_db/
│   ├── requirements.txt
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── .gitignore
```

---

# 💻 Prerequisites

Before running this project, install:

* Python 3.11 or later
* Node.js (v18 or later)
* npm
* Git

Verify installation:

```bash
python --version
node -v
npm -v
git --version
```

---

# 📥 Clone the Repository

```bash
git clone https://github.com/Sebin1806/rag-chatbot.git

cd rag-chatbot
```

---

# ⚙ Backend Setup

## Step 1 — Move into Backend

```bash
cd backend
```

---

## Step 2 — Create Virtual Environment

### Windows

```bash
python -m venv venv
```

### Linux / macOS

```bash
python3 -m venv venv
```

---

## Step 3 — Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Step 4 — Install Python Libraries

All required libraries are listed in **requirements.txt**.

Install everything using one command:

```bash
pip install -r requirements.txt
```

This installs packages such as:

* FastAPI
* Uvicorn
* ChromaDB
* Sentence Transformers
* Transformers
* Torch
* PyPDF
* Rank BM25
* NumPy
* and other dependencies

---

## Step 5 — Run Backend

```bash
uvicorn app.main:app --reload
```

Backend will start at:

```
http://127.0.0.1:8000
```

Swagger API documentation:

```
http://127.0.0.1:8000/docs
```

---

# 🌐 Frontend Setup

Open a new terminal.

Move into frontend folder:

```bash
cd frontend
```

---

## Install Node Modules

```bash
npm install
```

This automatically installs all frontend dependencies including:

* React
* Vite
* Axios
* Tailwind CSS

---

## Run Frontend

```bash
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# 🚀 Running the Complete Application

### Terminal 1

```bash
cd backend

venv\Scripts\activate

uvicorn app.main:app --reload
```

---

### Terminal 2

```bash
cd frontend

npm run dev
```

---

Open:

```
http://localhost:5173
```

---

# 📖 How to Use

1. Start backend server.
2. Start frontend server.
3. Open the application.
4. Upload one or more PDF documents.
5. Wait for document processing.
6. Ask questions in natural language.
7. The chatbot retrieves relevant information and generates context-aware answers.

---

# 🔄 Retrieval Workflow

```
User Question
      │
      ▼
Multi Query Retrieval
      │
      ▼
Hybrid Search
(Dense + BM25)
      │
      ▼
Cross Encoder Reranker
      │
      ▼
Neighbor Retrieval
      │
      ▼
Context Compression
      │
      ▼
LLM Response
```

---

# 📡 API Endpoints

| Method | Endpoint             | Description                  |
| ------ | -------------------- | ---------------------------- |
| GET    | /                    | Backend status               |
| GET    | /docs                | Swagger documentation        |
| POST   | /api/document/upload | Upload PDF                   |
| POST   | /api/chat/stream     | Chat with uploaded documents |

---

# 📦 Updating the Project

After making changes:

```bash
git add .

git commit -m "Describe your changes"

git push
```

---

# 🛠 Troubleshooting

## Python packages not installing

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

---

## Node modules missing

Run:

```bash
npm install
```

---

## Backend not starting

Check if the virtual environment is activated:

```bash
venv\Scripts\activate
```

---

## Frontend cannot connect to backend

Ensure:

Backend:

```
http://127.0.0.1:8000
```

Frontend:

```
http://localhost:5173
```

Both servers must be running.

---

# 🚀 Future Improvements

* HyDE (Hypothetical Document Embeddings)
* Query Routing
* Self-RAG
* Corrective RAG (CRAG)
* Agentic RAG
* Knowledge Graph Retrieval
* Citation Verification
* Multi-modal RAG
* Docker Support
* AWS Deployment

---

# 📸 Screenshots

Add screenshots here:

* Home Page
* PDF Upload
* Chat Interface
* Retrieval Logs

---

# 👨‍💻 Author

**Sebin S**

GitHub:
https://github.com/Sebin1806

LinkedIn:
https://www.linkedin.com/in/sebin1806/

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

# 📄 License

This project is licensed under the MIT License.
