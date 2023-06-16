from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from model import ModelTwo


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None


class ModelRequest(BaseModel):
    user_input: str


def load_model():
    global model
    model = ModelTwo()
    model.setup_time()


@app.on_event("startup")
async def startup_event():
    load_model()


@app.post("/predict")
async def predict(data: ModelRequest):
    if not model:
        load_model()

    user_input = data.user_input
    prediction = model.predict(user_input)
    return prediction


# if __name__ == "__main__":
#     uvicorn.run("ml_models.api_wrapper:app", host="0.0.0.0", port=8000, reload=True)




