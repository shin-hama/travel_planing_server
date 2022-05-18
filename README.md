# README

## deploy

```shell
gcloud functions deploy hello_http --trigger-http --allow-unauthenticated --runtime=python39 --env-vars-file .env.yaml
```

## local development

### debug

```shell
> functions_framework --target=hello_http --debug
```
