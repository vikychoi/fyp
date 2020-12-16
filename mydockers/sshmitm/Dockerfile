#FROM arm32v6/python:3.8-alpine
FROM python:3.8-alpine

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev make
RUN pip install --upgrade pip && pip install paramiko

RUN adduser -D sshmitm
USER sshmitm
COPY --chown=sshmitm ./src /src
WORKDIR /src
RUN chmod -R 777 /src


EXPOSE 3000

CMD python3 -u sshmitm.py
