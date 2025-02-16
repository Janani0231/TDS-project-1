from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
import tasksA
import json
import os

app = FastAPI()

class TaskRequest(BaseModel):
    task: str

def ensure_data_dir():
    """Ensure all required data directories exist."""
    dirs = [
        "data",
        "data/docs",
        "data/logs"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    ensure_data_dir()

@app.post("/run")
async def run_task(request: Request):
    try:
        # Get the task from the request
        task = request.query_params.get("task", "")
        task = task.strip()
        
        # Execute the appropriate task
        if "Install `uv`" in task:
            return {"status": "success", "result": tasksA.A1()}
        elif "format.md" in task:
            tasksA.A2()
            return {"status": "success"}
        elif "dates.txt" in task and "dates-wednesdays.txt" in task:
            tasksA.A3()
            return {"status": "success"}
        elif "contacts.json" in task and "contacts-sorted.json" in task:
            tasksA.A4()
            return {"status": "success"}
        elif "logs-recent.txt" in task:
            tasksA.A5()
            return {"status": "success"}
        elif "docs/index.json" in task:
            tasksA.A6()
            return {"status": "success"}
        elif "email.txt" in task and "email-sender.txt" in task:
            tasksA.A7()
            return {"status": "success"}
        elif "credit_card.png" in task and "credit-card.txt" in task:
            tasksA.A8()
            return {"status": "success"}
        elif "comments.txt" in task and "comments-similar.txt" in task:
            tasksA.A9()
            return {"status": "success"}
        elif "ticket-sales.db" in task and "ticket-sales-gold.txt" in task:
            tasksA.A10()
            return {"status": "success"}
        else:
            raise HTTPException(status_code=400, detail="Unknown task")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/read")
async def read_file(path: str):
    try:
        # Convert absolute paths to relative paths
        relative_path = path.replace("/data/", "data/")
        with open(relative_path, "r") as f:
            content = f.read()
            return Response(content=content, media_type="text/plain")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 