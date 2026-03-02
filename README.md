# Incident Copilot

Incident Copilot is a local incident triage assistant that uses Retrieval Augmented Generation (RAG) over runbooks to propose likely causes and next actions with evidence citations.

## What it does
- Ingests runbooks into a Qdrant vector database
- Retrieves the most relevant runbook chunks for an incident description
- Uses a local Ollama LLM to generate hypotheses and action steps
- Outputs citations to the exact retrieved chunks

## Tech stack
- Ollama (llama3.1:8b for generation, nomic-embed-text for embeddings)
- Qdrant (vector database, Docker)
- FastAPI + Uvicorn (API server)
- Python

## Setup

### 1) Prerequisites
Install and verify:
- Python 3.10+
- Docker Desktop
- Ollama

Verify installs:
```bash
docker --version
ollama --version
python --version
