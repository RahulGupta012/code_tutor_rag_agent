# Programming Tutor stack-overflow RAG

## Folder Structure

``` text
RAG/
├── app/
│   ├── assets/
│   ├── cache/
│   ├── chains/
│   ├── chat_history/
│   ├── embeddings/
│   ├── ingestion/
│   ├── LLM/
│   ├── prompts/
│   ├── retriever/
│   ├── services/
│   ├── utils/
│   ├── vector_store/
│   ├── __init__.py
│   └── main.py
├── evaluation/
├── frontend/
│   └── index.html
├── notebooks/
│   └── dataset_exploration.ipynb
├── tests/
│   └── test_quadrant.py
├── .dockerignore
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Overview

It is a Python Tutor RAG application that answers Python-related
questions using a hybrid retrieval pipeline.

The application retrieves relevant context from a local knowledge base
stored in Qdrant. When retrieval confidence is low, the pipeline can
fall back to web search before sending the final context to Gemini for
response generation.

# Python Tutor RAG

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-DC244C?logo=qdrant&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-LLM-8E75B2?logo=googlegemini&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging_Face-BGE_Embeddings-FFD21E?logo=huggingface&logoColor=black)
![DuckDuckGo](https://img.shields.io/badge/DuckDuckGo-Web_Search-DE5833?logo=duckduckgo&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)





## Main Features

-   Hybrid retrieval for Python questions
-   Qdrant vector database
-   BGE embedding model
-   BM25 retrieval
-   Confidence-based local knowledge base usage
-   Web search fallback
-   Gemini for answer generation
-   Query caching
-   FastAPI backend
-   Simple HTML frontend
-   Docker Compose setup
-   Retrieval evaluation scripts and tests

## Retrieval Flow

``` text
User Query
    ↓
Cache Lookup
    ↓
Hybrid Retrieval
    ├── Dense Retrieval
    └── BM25 Retrieval
    ↓
Confidence Check
    ├── High confidence → Local KB
    └── Low confidence  → Web Search
    ↓
Prompt Building
    ↓
Gemini
    ↓
Final Response
```

## Evaluation

The retrieval pipeline was tested on 10 queries.

![Evaluation Results](app/assets/readme_assets/evaluation.png)

## Application Logs

The logs below show application startup, Qdrant connection, embedding
model loading, hybrid retrieval, confidence checking, prompt
construction, and Gemini response generation.

![Application Logs](app/assets/readme_assets/logs.png)

## Run with Docker

``` bash
docker compose up --build
```

After the containers start, open the frontend in your browser and send a
Python-related query.

## Environment Variables

Create a `.env` file and add the required API keys and service
configuration used by the application.

