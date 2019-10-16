import io
import os
import uuid
import json
import logging
import datetime
import requests

from flask import Flask, request, Response
from cloudevents.sdk.event import v02
from cloudevents.sdk import marshaller
from cloudevents.sdk import converters

content_type = 'application/json'

webhook_url = os.environ['SLACK_WEBHOOK_URL']

app = Flask(__name__)
@app.route('/', methods=['POST'])
def event_handler():
  m = marshaller.NewDefaultHTTPMarshaller()
  event = m.FromRequest(
    v02.Event(),
    dict(request.headers),
    io.BytesIO(request.data),
    lambda x: json.loads(x.read())
  )
  (body, exist) = event.Get("data")
  app.logger.info(u'Event received:\n\t{}'.format(
      event.Properties(),
    )
  )
  if 'text_emojized' in body:
    message = body['emojized']
  elif 'text' in body:
    message = body['text']
  else:
    raise ValueError(
            'CloudEvent must have an "text_mojized" or "text" property'
    )
  response = Response(None, status=204)
  return response

def slackit(message):
  slack_data = {'text': message}
  response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
  )
  if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )

if __name__ != '__main__':
  # Redirect Flask logs to Gunicorn logs
  gunicorn_logger = logging.getLogger('gunicorn.error')
  app.logger.handlers = gunicorn_logger.handlers
  app.logger.setLevel(gunicorn_logger.level)
else:
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
