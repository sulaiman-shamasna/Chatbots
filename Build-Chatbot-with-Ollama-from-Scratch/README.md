# Build a Chatbot with Ollama from Scratch
---
This repo ilustrates a step-by-step implementation of a chatbot with advanced **Retrieval Augmented Generation - (RAG)** using [*Ollama*](https://ollama.com/) framework and **Llama** models.

## Architecture
---
![Chatbot Architecture](plots/architecture.svg)

## Code Structure
---
```
BUILD-CHATBOT-WITH-OLLAMA-FROM-SCRATCH
├── backend
│   ├── helpers
│   │   └── context_builder.py
│   ├── repositories
│   │   ├── __init__.py
│   │   └── sessions.py
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── embeddings
│   ├── Dockerfile
│   └── main.py
├── frontend
│   ├── Dockerfile
│   ├── main.py
│   └── __init__.py
├── docker-compose.yml
└── README.md
```
