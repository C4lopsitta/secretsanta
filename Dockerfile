FROM python:3.11.10-alpine
LABEL authors="c4lopsitta"

COPY . /app
COPY .env /app/.env

WORKDIR /app

RUN apk add busybox
RUN apk add busybox-extras
RUN pip install -r /app/requirements.txt

ENTRYPOINT ["uvicorn", "webpage:app", "--host", "0.0.0.0", "--port", "4040"]

