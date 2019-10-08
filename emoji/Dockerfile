FROM python:3.7-slim

WORKDIR /app
COPY requirements.txt app.py newemojis.json /app/

RUN pip install -r requirements.txt

ENV PORT=8080 \
    APP_HOME=/app \
	EMOJI_LANGUAGE=fr-CA

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
