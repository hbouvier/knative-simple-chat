#!/bin/sh

kubectl apply -f - <<EOF
apiVersion: serving.knative.dev/v1alpha1
kind: Service
metadata:
  name: ecouteur
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"

    spec:
      containers:
        - image: hbouvier/slack-command:$(cat VERSION.txt)
          env:
            - name: BROKER_URL
              value: ${BROKER_URL}
EOF
