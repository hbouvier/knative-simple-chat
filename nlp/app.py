import io
import os
import uuid
import json
import spacy
import logging
import datetime
from flask import Flask, request, Response
from cloudevents.sdk.event import v02
from cloudevents.sdk import marshaller
from cloudevents.sdk import converters

model = os.environ['SPACY_LANGUAGE_MODEL']
lang  = os.environ['SPACY_LANGUAGE']

nlp = spacy.load(model)

# Binary (Content-Type: application/json)
#       The CloudEvent envelop will be in HTTP Headers
#       The body of the request contains ONLY the "even data"
content_type = 'application/json'

app = Flask(__name__)
@app.route('/', methods=['POST'])
def event_handler():
  m = marshaller.NewDefaultHTTPMarshaller()
  event = m.FromRequest(
    v02.Event(),
    dict(request.headers),
    io.BytesIO(request.data),
    lambda x: json.loads(str(x.read()))
  )
  (body, exist) = event.Get("data")
  app.logger.info(u'Event received:\n\t{}'.format(
      event.Properties(),
    )
  )
  (status, payload) = process_event(body)

  hs, body = m.ToRequest(
    v02.Event()
      .SetContentType(content_type)
      .SetData(json.dumps(payload))
      .SetEventID(str(uuid.uuid4()))
      .SetSource('com.ruggedcode.chat.emoji')
      .SetEventTime('{}00Z'.format(datetime.datetime.utcnow().isoformat()))
      .SetEventType('com.ruggedcode.chat.message.text'),
    converters.TypeBinary, # use TypeStructured to push to an ESB
    lambda x: x
  )
  response = Response(body, status=status, headers=dict(hs))
  return response

def process_event(event):
  if 'text' in event:
    phrase = event['text']
    obj = lemmatize(phrase)
    event['lang'] = lang
    event['lemmas'] = obj['lemmas']
    event['tokens'] = obj['tokens']
    return 200, event
  else:
    return 400, {
      "status": "failed",
      "message" : "event must have 'text' property."
    }

def info(msg):
    app.logger.info(msg)

def get_custom_headers(headers):
  return { key : value for (key, value) in headers.items() if key[:3] == 'Ce-' or key[:2] == 'X-' }

def lemmatize(phrase):
  doc = nlp(phrase)
  lemmas = [token.lemma_ for token in doc]
  tokens = [token.text for token in doc]
  return {
    "lang": lang,
    "lemmas": lemmas,
    "tokens": tokens
  }

if __name__ != '__main__':
  # Redirect Flask logs to Gunicorn logs
  gunicorn_logger = logging.getLogger('gunicorn.error')
  app.logger.handlers = gunicorn_logger.handlers
  app.logger.setLevel(gunicorn_logger.level)
else:
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# SPACY_LANGUAGE_MODEL=fr_core_news_sm python s.py
# (sleep 15; curl http://localhost:8080/lemma -d '{"data":"je vais manger"}' -XPOST) &