#!/bin/sh

kubectl apply -f - <<EOF
apiVersion: serving.knative.dev/v1alpha1
kind: Service
metadata:
  name: slackit
spec:
  template:
    metadata:
#      name: slackit-v1
      annotations:
        autoscaling.knative.dev/minScale: "1"

    spec:
      containers:
        - image: hbouvier/slackit:$(cat VERSION.txt)
          env:
            - name: SLACK_WEBHOOK_URL
              value: ${SLACK_WEBHOOK_URL}
EOF
