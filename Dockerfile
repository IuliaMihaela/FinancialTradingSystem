# syntax=docker/dockerfile:1
FROM python:3.9-alpine

MAINTAINER feli n iulia

WORKDIR .

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["flask", "run"]