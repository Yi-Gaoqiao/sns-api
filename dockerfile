FROM python:3.7-alpine
LABEL architecture="Tsubasa"

ENV PYTHONUNBUFFERD 1

COPY ./requirements.txt /requirements.txt
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers
RUN pip install -r /requirements.txt

RUN mkdir /drf-sns
WORKDIR /drf-sns
COPY ./drf-sns /drf-sns

RUN adduser -D user
USER user