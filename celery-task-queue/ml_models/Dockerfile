FROM python:3.9-slim-buster
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app/
WORKDIR /app/
CMD ["uvicorn", "api_wrapper:app", "--host", "0.0.0.0", "--port", "8000"]