#/bin/sh
NAMESPACE=tutorial
URL=http://default-broker.${NAMESPACE}.svc.cluster.local/
HOST=cloudevents-logger.${NAMESPACE}.example.com
URL=${1:-knative}

curl -v -H "Host: ${HOST}" "${URL}"  -X POST -H "X-B3-Flags: 1"  -H "CE-SpecVersion: 0.2" -H "CE-Type: dev.knative.foo.bar" -H "CE-Time: 2019-10-05T03:56:24Z" -H "CE-ID: 45a8b444-3213-4758-be3f-540bf93f85ff" -H "CE-Source: dev.knative.example" -H 'CE-Datacontenttype: application/json' -H 'Content-Type: application/json' -d '{"text":"hello world"}'
