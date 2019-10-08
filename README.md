# knative-simple-chat
An echo chat example implemented with knative
=======
curl -v "http://chat-broker.henri.svc.cluster.local/" -X POST -H "X-B3-Flags:1"  -H "CE-SpecVersion:0.2" -H "CE-Type: com.ruggedcode.chat.message.text" -H "CE-Time:2018-04-05T03:56:24Z" -H "CE-ID:45a8b444-3213-4758-be3f-54093f85ff" -H "CE-Source: com.ruggedcode.chat.curl" -H 'Content-Type:application/json' -d '{"data":{"text":"trcuk"}}'
