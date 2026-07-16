# 🎓 AI Student Learning Assistant

An intelligent **AI-powered learning assistant** that helps students study smarter using **Retrieval-Augmented Generation (RAG)**, **LangGraph**, **Groq LLM**, **FAISS**, and **Streamlit**.

The assistant allows students to upload their own study PDFs and interact with them through multiple AI agents for explanations, summaries, quizzes, flashcards, study plans, and doubt solving.

---

# 🚀 Features

## 📖 Explain Topics
- Professor-style explanations
- Step-by-step learning
- Simple language
- Examples
- Advantages & disadvantages
- Applications
- Exam tips

---

## 📚 Chapter Summary
Automatically generates structured chapter summaries including:
- Overview
- Key Concepts
- Important Definitions
- Revision Notes
- Formula Section
- Viva Questions
- Exam Tips

---

## 📝 Quiz Generator
Creates university-level MCQs with:
- 10 Conceptual Questions
- Four Options
- Correct Answer
- Explanation

---

## 🃏 Flashcard Generator
Generates study flashcards containing:
- Question
- Answer
- Key Point
- Memory Trick

---

## 📅 Study Planner
Creates personalized study plans including:
- Topics
- Daily Schedule
- Revision Plan
- Priority
- Mock Test Day
- Final Revision

---

## 💬 Doubt Solver
Answers student questions only using the uploaded study material.

If the answer is unavailable in the uploaded PDF, the assistant responds honestly without hallucinating.

---

# 🧠 Technologies Used

| Category | Technology |
|----------|------------|
| Language | Python |
| Frontend | Streamlit |
| LLM | Groq (Llama 3.3 70B Versatile) |
| Workflow | LangGraph |
| Retrieval | RAG |
| Vector Database | FAISS |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| PDF Processing | PyMuPDF |
| Environment | python-dotenv |

---

# 🏗 Project Architecture

```
                 Student

                    │

                    ▼

             Streamlit UI

                    │

                    ▼

            LangGraph Router

     ┌────────┬────────┬────────┐
     │        │        │        │
     ▼        ▼        ▼        ▼

 Teacher   Summary   Quiz   Flashcards

     │        │        │        │

     └────────┴────────┴────────┘

                ▼

          Study Planner

                ▼

          Doubt Solver

                ▼

          RAG Pipeline

                ▼

        Hybrid Retrieval

      (Semantic + Keyword)

                ▼

          FAISS Database

                ▼

      Uploaded PDF Documents
```

---

# 📂 Project Structure

```
AI-Student-Learning-Assistant
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── src
│   ├── agents
│   ├── graph
│   ├── models
│   ├── prompts
│   ├── rag
│   └── utils
│
├── data
│
├── tests
│
└── logs
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/sherishacv/AI-Student-Learning-Assistant.git

cd AI-Student-Learning-Assistant
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create Environment File

Create a file named

```
.env
```

Add

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY

GROQ_MODEL=llama-3.3-70b-versatile

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHUNK_SIZE=1200

CHUNK_OVERLAP=200

TOP_K=5

HYBRID_ALPHA=0.75
```

---

## Run Application

```bash
streamlit run app.py
```

---

# 📸 Application Workflow

1. Upload Study PDFs
2. Index Documents
3. Generate Embeddings
4. Store in FAISS
5. Retrieve Relevant Chunks
6. Route Query using LangGraph
7. AI Agent Generates Response
8. Display Answer with Sources

---

# 🔍 Retrieval Pipeline

```
PDF

↓

Loader

↓

Chunking

↓

Embeddings

↓

FAISS Vector Store

↓

Hybrid Retrieval

↓

LangGraph Router

↓

Selected AI Agent

↓

Groq LLM

↓

Response
```

---

# 🛡 Security Features

- Prompt Injection Protection
- Hallucination Reduction
- Uses Only Uploaded Study Material
- Citation-Based Responses
- No Hidden Prompt Leakage
- Environment Variable Protection

---

# 📊 Current Features

- PDF Upload
- RAG Retrieval
- FAISS Search
- Hybrid Retrieval
- LangGraph Routing
- Teacher Agent
- Summary Agent
- Quiz Generator
- Flashcard Generator
- Study Planner
- Doubt Solver
- Conversation History
- Confidence Score
- Source Citations

---

# 🎯 Future Improvements

- Voice-based Interaction
- OCR for Images
- Multiple PDF Collections
- Multi-language Support
- AI Generated Mind Maps
- PDF Export
- PPT Generation
- Mobile Responsive UI

---

# 👩‍💻 Developer

**Sherisha C V**

Artificial Intelligence & Data Science

BMS College of Engineering

GitHub:
https://github.com/sherishacv

---

# ⭐ If you found this project useful

Please consider giving this repository a ⭐ on GitHub.

---

# 📜 License

This project is developed for educational and academic purposes.
