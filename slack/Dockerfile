FROM python:3.7-slim

WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt

ENV PORT=8080 \
    APP_HOME=/app

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
