from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from tasks import run_prediction
from celery.result import AsyncResult


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PushRequest(BaseModel):
    input: str


@app.post("/push")
async def push(request: PushRequest):
    user_input = request.input
    print("user input push: ", user_input)
    task_id = run_prediction.delay(user_input=user_input)
    return {'id': str(task_id)}


@app.get("/status/{id}")
async def get_job_status(id: str):
    task = AsyncResult(id)
    return {"status": task.status}


@app.get("/data/{id}")
async def get_job_data(id: str):
    task = AsyncResult(id)
    if not task.ready():
        return {"msg": "task not processed yet", "status": task.status}
    result = task.get()
    return {"result": result}


# if __name__ == "__main__":
#     uvicorn.run("core_api.api:app", host="0.0.0.0", port=8001, reload=True)
