import os
from celery import Celery
import requests


BROKER_URI = os.getenv("BROKER_URI") or "redis://localhost:6379"
BACKEND_URI = os.getenv("BACKEND_URI") or "redis://localhost:6379"

app = Celery(
    'celery_app',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['core_api.tasks']
)

app.conf.task_acks_late = True  # Allow tasks to be acknowledged after they are completed
app.conf.task_reject_on_worker_lost = True  # Reject tasks when worker connection is lost
app.conf.task_default_retry_delay = 30  # Retry delay in seconds
app.conf.task_max_retries = 3  # Maximum number of retries

# Set the default queue
app.conf.task_default_queue = 'default'


@app.task(name='tasks.run_prediction')
def run_prediction(user_input: str):
    response = requests.post("http://0.0.0.0:8000/predict", json={"user_input": user_input})
    output = response.json()
    return output