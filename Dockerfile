FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /backend_app
WORKDIR /backend_app

COPY . .

RUN pip install -U pip 
RUN pip install -r requirements.txt

# RUN chmod a+x scripts/*.sh
