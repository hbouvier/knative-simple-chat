import io
import os
import uuid
import json
import logging
import datetime
from flask import Flask, request, Response
from cloudevents.sdk.event import v02
from cloudevents.sdk import marshaller
from cloudevents.sdk import converters

lang  = os.environ['EMOJI_LANGUAGE']

input_content_type = 'application/cloudevents+json'
output_content_type = 'application/json'

app = Flask(__name__)
@app.route('/', methods=['POST'])
def event_handler():
  m = marshaller.NewDefaultHTTPMarshaller()
  patched_headers = dict(request.headers)
  patched_headers['Content-Type'] = input_content_type
  event = m.FromRequest(
    v02.Event(),
    patched_headers,
    io.BytesIO(request.data),
    lambda x: x
  )
  (body, exist) = event.Get("data")
  app.logger.info(u'Event received:\n\t{}'.format(
      event.Properties(),
    )
  )
  (status, payload) = process_event(body)

  hs, body = m.ToRequest(
    v02.Event()
      .SetContentType('application/cloudevents+json')
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
  if 'lemmas' in event and 'tokens' in event:
    words = emojize_lemmas(lang, event['lemmas'], event['tokens'])
    event['lang'] = lang
    event['text_emojized'] = ' '.join(words)
    event['emojized'] = words
    return 200, payload
  elif 'text' in event:
    phrase = event['text']
    obj = emojize_phrase(lang, phrase)
    event['lang'] = lang
    event['text_emojized'] = ' '.join(obj['emojized'])
    event['emojized'] = obj['emojized']
    return 200, payload
  else:
    return 400, {
      "status": "failed",
      "message" : "event must have either a 'text' property or 'lemmas' and 'tokens'."
    }

def info(msg):
    app.logger.info(msg)

def get_custom_headers(headers):
  return { key : value for (key, value) in headers.items() if key[:3] == 'Ce-' or key[:2] == 'X-' }

def loadfile(filename):
  with open(filename) as json_file:
    data = json.load(json_file)
  return data

def emojize_phrase(lang, phrase):
  return {
    "lang"     : lang,
    "phrase"   : phrase,
    "emojized" : emojize_words(lang, phrase.split())
  }

def emojize_lemmas(lang, lemmas, tokens):
  return [emojize_lemma(lang, lemmas[i], tokens[i]) for i in range(len(lemmas))]

def emojize_lemma(lang, lemma, token):
  emoji = emojize(lang, lemma)
  if emoji == lemma:
    return token
  return emoji


def emojize_words(lang, words):
  return [emojize(lang, word) for word in words]

def emojize(lang, word):
  lword = word.lower()
  for key in emojis:
    emoji = emojis[key]

    keywords = emoji[lang]
    if word == key or word in keywords:
      return emoji['char']
  return word

emojis = loadfile('newemojis.json')

if __name__ != '__main__':
  # Redirect Flask logs to Gunicorn logs
  gunicorn_logger = logging.getLogger('gunicorn.error')
  app.logger.handlers = gunicorn_logger.handlers
  app.logger.setLevel(gunicorn_logger.level)
else:
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
