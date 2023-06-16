from celery_runner.runner import app
import requests


@app.task(name='tasks.run_prediction')
def run_prediction(user_input: str):
    response = requests.post("http://0.0.0.0:8000/predict", json={"user_input": user_input})
    output = response.json()
    return output

