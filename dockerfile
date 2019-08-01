FROM python:3.7-alpine

RUN apk update && apk add build-base

RUN pip install --no-cache-dir -U setuptools pip

RUN pip install --no-cache-dir -U pyonedesk

CMD [ "pyonedesk", "info" ]