import io
import os
import uuid
import json
import logging
import requests
import datetime
from flask import Flask, request, Response
from cloudevents.sdk.event import v02
from cloudevents.sdk import marshaller
from cloudevents.sdk import converters

content_type = 'application/json'
webhook_url = os.environ['BROKER_URL']

app = Flask(__name__)
@app.route('/', methods=['POST'])
def event_handler():
  # Parse the parameters you need
  token = request.form.get('token', None)  # TODO: validate the token
  command = request.form.get('command', None)
  text = request.form.get('text', None)
  # Validate the request parameters
  if not token:  # or some other failure condition
    abort(400)

  app.logger.info(u'slack command received:\n\t{}'.format(
      text
    )
  )
  m = marshaller.NewDefaultHTTPMarshaller()
  hs, body = m.ToRequest(
    v02.Event()
      .SetContentType(content_type)
      .SetData(json.dumps({"text": text}))
      .SetEventID(str(uuid.uuid4()))
      .SetSource("com.ruggedcode.chat.slack")
      .SetEventTime("{}00Z".format(datetime.datetime.utcnow().isoformat()))
      .SetEventType("com.ruggedcode.chat.message.text"),
    converters.TypeBinary, # use TypeStructured to push to an ESB
    lambda x: x
  )

  response = requests.post(
    webhook_url,
    headers=dict(hs),
    data=body
  )
  app.logger.info(u'Slacking \n\t{}\n\tCODE: {}'.format(body, response.status_code))
  app.logger.info(u'data:\n\t{}'.format(response.text))
  if response.status_code < 200 or  response.status_code > 204:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )

  response = Response(None, status=204)
  # response = Response(body, status=200, headers=dict(hs))
  return response

if __name__ != '__main__':
  # Redirect Flask logs to Gunicorn logs
  gunicorn_logger = logging.getLogger('gunicorn.error')
  app.logger.handlers = gunicorn_logger.handlers
  app.logger.setLevel(gunicorn_logger.level)
else:
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
