FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt


CMD ["celery", "-A", "celery_app.celery_worker", "worker", "--loglevel=info", "--pool=solo"]
