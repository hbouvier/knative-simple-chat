FROM hbouvier/spacy_fr:v3.7
# FROM python:3.7-slim

WORKDIR /app
COPY requirements.txt *.py /app/

RUN pip install -r requirements.txt

ENV PORT=8080 \
    APP_HOME=/app \
	SPACY_LANGUAGE=fr-CA \
    SPACY_LANGUAGE_MODEL=fr_core_news_sm

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
