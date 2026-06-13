# Stephen Hawking Digital Twin

A Retrieval-Augmented Generation (RAG) based AI Digital Twin of Stephen Hawking built using Gemini 2.5 Flash, ChromaDB, Streamlit, and memory modules.

The project simulates conversations with Stephen Hawking by combining:

* A curated knowledge base consisting of books, interviews, lectures, and transcripts
* Retrieval-Augmented Generation (RAG)
* Short-term conversational memory
* Long-term user memory
* A Stephen Hawking persona prompt
* A Streamlit-based interactive interface

The goal is to create a system that not only answers questions accurately using Hawking-related sources but also responds in a style consistent with Stephen Hawking's public persona.

---

# Features

### Retrieval-Augmented Generation (RAG)

The system retrieves relevant information from a custom Stephen Hawking knowledge base before generating responses.

Sources include:

* A Brief History of Time
* Interviews
* Lectures
* Biographical material
* Research-related documents

### Persona Consistency

Responses are generated using a dedicated Stephen Hawking system prompt to maintain a consistent tone, style, and personality.

### Short-Term Memory

The assistant remembers recent conversation turns to maintain context throughout a session.

### Long-Term Memory

Important user facts can be stored and reused across conversations.

Examples:

* User name
* Profession
* Interests
* Academic background

### Source Attribution

The application displays the source documents used to answer each query, providing transparency and demonstrating RAG functionality.

### Interactive Web Interface

Built using Streamlit with:

* Chat interface
* Memory dashboard
* Conversation reset
* Long-term memory management

---

# System Architecture

The architecture consists of four primary layers:

## 1. Data Ingestion Layer

Source documents are loaded and processed.

Steps:

1. Document Loading
2. Text Extraction
3. Chunking
4. Metadata Generation
5. Embedding Creation

---

## 2. Vector Database Layer

Embeddings are stored inside ChromaDB.

The vector store enables semantic search across all Stephen Hawking documents.

---

## 3. Core RAG Pipeline

When a user asks a question:

1. Query is embedded
2. Relevant chunks are retrieved from ChromaDB
3. Retrieved context is combined with:

   * Short-term memory
   * Long-term memory
   * Persona prompt
4. Gemini 2.5 Flash generates the final response

---

## 4. Interface Layer

Streamlit presents:

* Chat interface
* Retrieved source display
* Memory dashboard
* Reset controls

---

# Project Structure

```text
DigitalTwin/
│
├── app.py
├── agent.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── architecture/
│   └── architecture_diagram.png
│
├── assets/
│   └── hawking.jpg
│
├── data/
│   └── sources/
│
├── memory/
│   ├── short_term.py
│   └── long_term.py
│
├── persona/
│   └── system_prompt.py
│
├── rag/
│   ├── ingest.py
│   └── retriever.py
│
└── chroma_db/
```

---

# Technologies Used

* Python
* Streamlit
* Google Gemini 2.5 Flash
* ChromaDB
* Sentence Transformers
* LangChain
* PyMuPDF
* Python Dotenv

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd DigitalTwin
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# API Configuration

Create a `.env` file in the root directory.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Obtain a Gemini API key from Google AI Studio.

---

# Preparing the Knowledge Base

Place Stephen Hawking source documents inside:

```text
data/sources/
```

Examples:

* Books
* Interviews
* Lecture transcripts
* Articles
* PDFs

---

# Build Vector Database

Run:

```bash
python rag/ingest.py
```

This will:

* Process documents
* Create embeddings
* Store vectors inside ChromaDB

---

# Running the Application

Launch Streamlit:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

Typically:

```text
http://localhost:8501
```

---

# Example Questions

Examples:

* What is Hawking Radiation?
* What did you discuss in your CNN interview?
* What is the central idea of A Brief History of Time?
* What were your views on God?
* Tell me about black holes.
* What is the origin of the universe?

---

# Memory Functionality

The system maintains:

## Short-Term Memory

Stores recent conversation history during a session.

## Long-Term Memory

Stores important user facts and preferences for future interactions.

---

# Future Improvements

Potential enhancements include:

* Voice interaction
* Speech synthesis
* Better memory extraction
* Automatic citation generation
* Advanced document reranking
* Multi-scientist support
* Knowledge graph integration

---

