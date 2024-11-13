FROM python:3.10.10-alpine
LABEL authors="c4lopsitta"

COPY . /app
COPY .env /app/.env

WORKDIR /app

RUN pip install -r /app/requirements.txt

ENTRYPOINT ["uvicorn", "webpage:app", "--host", "0.0.0.0", "--port", "4040"]

