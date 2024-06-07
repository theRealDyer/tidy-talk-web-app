FROM python:3.9

COPY requirements.txt /app/
COPY src/ /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 3600 app:app