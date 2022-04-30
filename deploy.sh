#!/bin/sh

poetry export -o requirements.txt --without-hashes

gcloud functions deploy hello_http \
  --trigger-http \
  --allow-unauthenticated \
  --region=asia-northeast1 \
  --runtime=python39 \
  --env-vars-file .env.yaml
