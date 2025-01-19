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
## Usage
---
Working with this project requires familiarity with ```Docker```. If you're in a windows machine, please make sure to have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.

To test this project, please follow the steps bellow:
1. Clone the project repo and navigate to the corresponding work directory of the ```ollama-based``` project, using the command:
    ```bash
    git clone https://github.com/sulaiman-shamasna/Chatbots && cd Build-Chatbot-with-Ollama-from-Scratch/
    ```
2. Make sure docker demon is running, and build the docker images:

    ```
    docker -f frontend/Dockerfile -t sulaiman/ollama-frontend:1.0 .
    ```

    ```
    docker -f backend/Dockerfile -t sulaiman/ollama-backend:1.0 .
    ```

    ```
    docker -f embeddings/Dockerfile -t sulaiman/ollama-embeddings:1.0 .
    ```
3. Run the ```docker-compose.yml``` file, usingi the command:
    
    ```
    docker-compose up --build
    ```