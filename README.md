# 🤖 ProcureAI — Intelligent Procurement Knowledge Assistant

ProcureAI is an AI-powered procurement knowledge assistant built using Python, Generative AI, Retrieval-Augmented Generation (RAG), and AI agents.

The application demonstrates how artificial intelligence can assist with company policy retrieval, procurement calculations, and support-ticket classification.

## Features

- General AI chatbot
- Conversation memory
- Document-based question answering
- Retrieval-Augmented Generation (RAG)
- Semantic search using embeddings
- FAISS vector storage
- History-aware retrieval
- AI agents and function calling
- Purchase cost calculation
- Purchase approval checking
- Structured JSON output
- API exception handling
- Interactive Streamlit frontend

## Technology Stack

| Technology     | Purpose                      |
| -------------- | ---------------------------- |
| Python         | Application development      |
| OpenAI API     | LLM integration              |
| LangChain      | RAG and AI agents            |
| Hugging Face   | Text embeddings              |
| FAISS          | Vector similarity search     |
| Pydantic       | Structured output validation |
| Streamlit      | Web interface                |
| Pytest         | Automated testing            |
| Git and GitHub | Version control              |

## Project Architecture

User → Streamlit Interface → Python Backend → LLM / RAG / AI Agent → Response

### RAG Pipeline

Document → Text Chunking → Embeddings → FAISS → Retrieval → LLM → Answer

## Project Structure

- app.py — Streamlit interface
- config.py — Environment configuration
- llm.py — LLM integration and structured outputs
- rag.py — Document retrieval pipeline
- agent.py — AI agent and business tools
- knowledge.txt — Fictional company knowledge
- test_app.py — Automated tests
- requirements.txt — Project dependencies

## Installation

Clone the repository:

`git clone https://github.com/shankar1242003/procureai.git`

Navigate to the project:

`cd procureai`

Create a virtual environment:

`python -m venv .venv`

Install dependencies:

`pip install -r requirements.txt`

Configure authorized API credentials in a local .env file.

Run the application:

`python -m streamlit run app.py`

## Testing

`python -m pytest -v`

## Application Modes

### General AI

Answers general questions using an LLM and conversation history.

### Document Q&A

Retrieves relevant company policies using RAG.

### AI Agent

Performs purchase calculations, approval checks, and policy retrieval using Python tools.

### Ticket Classification

Converts support tickets into structured JSON responses.

## Future Improvements

- Docker containerization
- Cloud deployment
- FastAPI backend
- PDF document uploads
- PostgreSQL database
- User authentication
- Hybrid search and reranking
- CI/CD pipeline

## Disclaimer

This is an independent educational portfolio project using fictional company data. It is not affiliated with Zycus and does not execute actual procurement transactions.
