from runner import app
import requests
import os


@app.task(name='tasks.run_prediction')
def run_prediction(user_input: str):
    model_base_uri = os.getenv('MODEL_URI')
    response = requests.post(f"{model_base_uri}/predict", json={"user_input": user_input})
    output = response.json()
    return output

