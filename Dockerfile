FROM python:3.11.10-alpine
LABEL authors="c4lopsitta"

COPY . /app
COPY .env /app/.env

WORKDIR /app

RUN apk add busybox
RUN apk add busybox-extras
RUN apk add curl
RUN pip install -r /app/requirements.txt

ENTRYPOINT ["uvicorn", "webpage:app", "--host", "0.0.0.0", "--port", "9090", "--workers", "6"]

