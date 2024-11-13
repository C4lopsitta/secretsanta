FROM python:3.10.10-alpine
LABEL authors="c4lopsitta"

COPY . /app
COPY .env /app/.env


EXPOSE 4040:4040
WORKDIR /app

RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip install -r /app/requirements.txt

ENTRYPOINT ["uvicorn", "webpage:app", "--host", "0.0.0.0", "--port", "4040"]

