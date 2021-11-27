# syntax=docker/dockerfile:1

FROM python:3.7.10-slim-stretch

WORKDIR /py_twitter-posts-scraper

COPY requirements.txt requirements.txt

COPY crontab crontab

RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get -y install cron

COPY . .

RUN crontab crontab

CMD ["cron", "-f"]
