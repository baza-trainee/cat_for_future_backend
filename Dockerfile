FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /backend_app
WORKDIR /backend_app

RUN pip install -U pip 

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
