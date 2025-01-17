# Use a lightweight Python image
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x start.sh

ENTRYPOINT ["sh", "start.sh"]
