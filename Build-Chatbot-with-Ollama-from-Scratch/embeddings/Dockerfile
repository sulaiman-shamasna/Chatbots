FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    pip install --no-cache-dir --upgrade \
        faiss-cpu==1.9.0.post1 \
        fastapi==0.115.6 \
        pydantic==2.10.5 \
        sentence-transformers==3.3.1
COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]