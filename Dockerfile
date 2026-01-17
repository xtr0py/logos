FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py

COPY config/quotes.json /app/quotes.seed.json

RUN mkdir -p /config

ENV QUOTES_PATH=/config/quotes.json
EXPOSE 8000

CMD ["sh", "-c", "mkdir -p /config && if [ ! -s /config/quotes.json ]; then cp /app/quotes.seed.json /config/quotes.json; fi && exec uvicorn app:app --host 0.0.0.0 --port 8000"]
