# Lab: RAG AI Assistant – Retrieval-Augmented Generation System

## Overview
Build a production-ready AI assistant using Retrieval-Augmented Generation (RAG). This lab covers document ingestion, vector embeddings, semantic search, and integrating a large language model for question answering.

## Architecture

```
Documents --> Embedding Model --> Vector Store
User Query --> Embedding Model --> Vector Store (similarity search) --> LLM --> Response
```

See `architecture.png` for a detailed component diagram.

## Learning Objectives
- Ingest and chunk documents into a vector database.
- Generate and query vector embeddings for semantic search.
- Integrate an LLM API to produce context-grounded responses.

## Prerequisites
- Python 3.10+.
- An OpenAI API key (or compatible local model).
- Docker installed locally.

## Getting Started

1. Install dependencies from `starter-code/requirements.txt`:
   ```bash
   pip install -r starter-code/requirements.txt
   ```
2. Set your API key:
   ```bash
   export OPENAI_API_KEY=<your-key>
   ```
3. Ingest sample documents:
   ```bash
   python ingest.py --docs data/sample_docs/
   ```
4. Run the assistant:
   ```bash
   python assistant.py
   ```
5. Ask a question and verify the response is grounded in the ingested documents.

## Deliverables
- A working RAG pipeline that answers questions based on custom documents.
- A brief analysis comparing retrieval-augmented responses to vanilla LLM responses.

## Solution
See the `solution/` directory for a reference implementation.
