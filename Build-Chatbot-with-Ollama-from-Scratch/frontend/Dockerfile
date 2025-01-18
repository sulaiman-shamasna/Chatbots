FROM python:3.10

WORKDIR /app

RUN apt-get update && \
    pip install --no-cache-dir --upgrade \
        streamlit==1.41.1 \
        requests==2.32.3 \
        python-dotenv==1.0.1

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
