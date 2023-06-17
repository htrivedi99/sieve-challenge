import os
from celery import Celery
import time
import requests


BROKER_URI = os.getenv("BROKER_URI") or "redis://localhost:6379"
BACKEND_URI = os.getenv("BACKEND_URI") or "redis://localhost:6379"

app = Celery(
    'celery_app',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['tasks']
)

app.conf.task_acks_late = True  # Allow tasks to be acknowledged after they are completed
app.conf.task_reject_on_worker_lost = True  # Reject tasks when worker connection is lost
app.conf.task_default_retry_delay = 30  # Retry delay in seconds
app.conf.task_max_retries = 3  # Maximum number of retries
app.conf.task_default_queue = 'default'  # Set the default queue
app.conf.task_track_started = True


@app.task(name='tasks.run_prediction')
def run_prediction(user_input: str, start_time: float):
    try:
        model_base_uri = os.getenv('MODEL_URI')
        response = requests.post(f"{model_base_uri}/predict", json={"user_input": user_input})
        output = response.json()
        end_time = time.time()
        latency = end_time - start_time  # latency is in seconds
        output["latency"] = latency
        return output
    except Exception as e:
        raise e  # Need to raise exception in order to trigger retry

