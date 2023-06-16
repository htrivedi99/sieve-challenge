import uuid
import time
import random


class ModelTwo:
    def __init__(self):
        time.sleep(self.setup_time())
        self.return_val = "world" + str(uuid.uuid4())

    def predict(self, hello: str):
        time.sleep(self.predict_time())
        return {"output": self.return_val, "input": hello}

    def setup_time(self):
        return random.randint(2, 40)

    def predict_time(self):
        return random.randint(5, 25)

