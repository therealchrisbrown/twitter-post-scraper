# syntax=docker/dockerfile:1

FROM python:3.7.10-slim-stretch

WORKDIR /twitter-scraper

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN apt-get update 

COPY . .

ENV PORT 8080

CMD ["python3", "twitter-post-scraper.py"]
