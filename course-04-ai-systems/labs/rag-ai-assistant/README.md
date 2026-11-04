# Lab: RAG AI Assistant – Retrieval-Augmented Generation System

## Overview
Build a production-ready AI assistant using Retrieval-Augmented Generation (RAG). This lab covers document ingestion, vector embeddings, semantic search, and integrating a large language model for question answering.

## Architecture

```
Documents --> Embedding Model --> Vector Store
User Query --> Embedding Model --> Vector Store (similarity search) --> LLM --> Response
```

## Learning Objectives
- Ingest and chunk documents into a vector database.
- Generate and query vector embeddings for semantic search.
- Integrate an LLM API to produce context-grounded responses.

## Prerequisites
- Python 3.10+.
- No API key required for the default local retrieval mode.

## Getting Started

1. Install dependencies:
   ```bash
   cd starter-code
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Ingest sample documents:
   ```bash
   python ingest.py --docs data/sample_docs --out data/index.pkl
   ```
3. Ask a question:
   ```bash
   python assistant.py --index data/index.pkl --question "What is RAG and why use it?"
   ```

## Validation

- You should see the retrieved passages printed with source citations.
- The final answer should reference only retrieved text (no hallucinated facts).

## Experiment

1. Change chunk size and overlap (in `rag/chunking.py`) and compare retrieval quality.
2. Change `--top-k` in `assistant.py` and observe precision vs recall.

## Deliverables
- A working RAG pipeline that answers questions based on custom documents.
- A brief analysis comparing retrieval-augmented responses to vanilla LLM responses.

## Solution

```bash
cd solution
pip install -r requirements.txt
python ingest.py --docs data/sample_docs --out data/index.pkl
python assistant.py --index data/index.pkl --question "What is RAG and why use it?"
```

The reference answer is extractive: it prints retrieved chunks and a short citation, and it does not call an external model. Swap in an LLM only after the retrieved context is the thing you want the model to see.


