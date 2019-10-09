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
  hs, body = m.ToRequest(
    v02.Event()
      .SetContentType(content_type)
      .SetData(json.dumps(body))
      .SetEventID(str(uuid.uuid4()))
      .SetSource("com.ruggedcode.cloudevents")
      .SetEventTime("{}00Z".format(datetime.datetime.utcnow().isoformat()))
      .SetEventType("com.ruggedcode.cloudevents.logger"),
    converters.TypeBinary, # use TypeStructured to push to an ESB
    lambda x: x
  )
  response = Response(body, status=200, headers=dict(hs))
  return response

if __name__ != '__main__':
  # Redirect Flask logs to Gunicorn logs
  gunicorn_logger = logging.getLogger('gunicorn.error')
  app.logger.handlers = gunicorn_logger.handlers
  app.logger.setLevel(gunicorn_logger.level)
else:
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
