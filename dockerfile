FROM python:3.7-alpine
LABEL architecture="Tsubasa"

ENV PYTHONUNBUFFERD 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /drf-sns
WORKDIR /drf-sns
COPY ./drf-sns /drf-sns

RUN adduser -D user
USER user