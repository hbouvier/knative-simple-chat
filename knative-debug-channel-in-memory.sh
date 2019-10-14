kubectl --namespace knative-eventing logs -l messaging.knative.dev/channel=in-memory-channel,messaging.knative.dev/role=dispatcher -c dispatcher -f
