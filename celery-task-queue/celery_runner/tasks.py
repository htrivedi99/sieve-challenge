from runner import app
import requests
import os
import time


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

