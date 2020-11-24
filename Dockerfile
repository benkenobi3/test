FROM python:3.8-alpine

WORKDIR /app

RUN apk update && \
    apk add --no-cache --virtual build-deps gcc make musl-dev python3-dev jpeg-dev zlib-dev libffi-dev && \
    pip install --upgrade pip==20.2.4

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt && \
    apk del build-deps

ENV PORT=80

WORKDIR /app/src
COPY . /app/

ENTRYPOINT ["../docker-entrypoint.sh"]
