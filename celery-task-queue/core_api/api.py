from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
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


@app.on_event("shutdown")
def shutdown_event():
    print("shutting down fast api server")


@app.post("/push")
async def push(request: PushRequest):
    user_input = request.input
    print("user input push: ", user_input)
    start_time = time.time()
    task_id = run_prediction.delay(user_input=user_input, start_time=start_time)
    return {'id': str(task_id)}


@app.get("/status/{id}")
async def get_job_status(id: str):
    task = AsyncResult(id)
    status = ""
    if task.status == "PENDING":
        status = "queued"
    elif task.status == "STARTED":
        status = "processing"
    elif task.status == "SUCCESS":
        status = "finished"
    elif task.status == "FAILURE":
        status = "error"
    return {"status": status}


@app.get("/data/{id}")
async def get_job_data(id: str):
    task = AsyncResult(id)
    if not task.ready():
        return {"msg": "task not processed yet", "status": task.status}
    result = task.get()
    return result


# if __name__ == "__main__":
#     uvicorn.run("core_api.api:app", host="0.0.0.0", port=8001, reload=True)
