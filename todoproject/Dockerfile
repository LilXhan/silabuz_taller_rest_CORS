FROM python:3.11.1-alpine3.17 

RUN apk update && apk add --no-cache --virtual .build-deps \
    gcc libffi-dev postgresql-dev musl-dev 

WORKDIR /app/

COPY requirements.txt /app/requirements.txt 

RUN pip install --upgrade --no-cache-dir -r requirements.txt

COPY . /app/