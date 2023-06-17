import os
from celery import Celery, signals


BROKER_URI = os.getenv("BROKER_URI") or "redis://localhost:6379"
BACKEND_URI = os.getenv("BACKEND_URI") or "redis://localhost:6379"

BROKERS = [
    BROKER_URI,
    "redis://redis-1.redis.sieve.svc.cluster.local:6379",
    "redis://redis-2.redis.sieve.svc.cluster.local:6379"
]

app = Celery(
    'celery_app',
    broker=BROKERS,
    backend=BACKEND_URI,
    include=['tasks']
)

app.conf.task_acks_late = True  # Allow tasks to be acknowledged after they are completed
app.conf.task_reject_on_worker_lost = True  # Reject tasks when worker connection is lost
app.conf.task_default_retry_delay = 30  # Retry delay in seconds
app.conf.task_max_retries = 3  # Maximum number of retries
app.conf.task_default_queue = 'default'  # Set the default queue
app.conf.task_track_started = True


def handle_sigterm(sender, **kwargs):
    print("Received SIGTERM signal. Performing cleanup...")
    worker = sender
    active_tasks = worker.app.control.inspect().active()
    if active_tasks:
        task_ids = [task['id'] for worker_tasks in active_tasks.values() for task in worker_tasks]
        worker.app.send_task('celery.accumulate', args=(task_ids,), kwargs={'routing_key': 'default'})

    # Terminate the worker gracefully
    sender.terminate()


signals.worker_shutdown.connect(handle_sigterm)

