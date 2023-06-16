FROM python:3.9-slim-buster
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY runner.py /app/
WORKDIR /app/
CMD celery -A runner worker --loglevel=info
