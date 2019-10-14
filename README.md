# knative-simple-chat
An echo chat example implemented with knative
=======
curl -v "http://chat-broker.henri.svc.cluster.local/" -X POST -H "X-B3-Flags:1"  -H "CE-SpecVersion:0.2" -H "CE-Type: com.ruggedcode.chat.message.text" -H "CE-Time:2018-04-05T03:56:24Z" -H "CE-ID:45a8b444-3213-4758-be3f-54093f85ff" -H "CE-Source: com.ruggedcode.chat.curl" -H 'Content-Type:application/json' -d '{"data":{"text":"trcuk"}}'


wget https://github.com/cppforlife/knctl/releases/download/v0.3.0/knctl-linux-amd64
mv knctl-linux-amd64 knctl
chmod a+x knctl

kubectl -n default create serviceaccount eventing-broker-ingress
kubectl -n default create serviceaccount eventing-broker-filter
kubectl -n default create rolebinding eventing-broker-ingress \
  --clusterrole=eventing-broker-ingress \
  --user=eventing-broker-ingress
kubectl -n default create rolebinding eventing-broker-filter \
  --clusterrole=eventing-broker-filter \
  --serviceaccount=default:eventing-broker-filter

  transform map 
    fixed = {k: f(v) for k, v in hs.items()}
    