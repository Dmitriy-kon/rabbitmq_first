FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


COPY ./requirements.txt /app

RUN pip install -r requirements.txt
RUN pip install aiormq
RUN pip freeze > requirements.txt

COPY . ./

