from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from scripts import train, evaluate, retrain
from utils import monitor
import shutil
import os

app = FastAPI()

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

class MonitorInput(BaseModel):
    threshold: float

@app.post("/train/")
async def trigger_train(file: UploadFile = File(...)):
    file_path = os.path.join(DATA_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    train.train_model(file_path)
    return {"message": "Model trained successfully"}

@app.post("/retrain/")
async def trigger_retrain(file: UploadFile = File(...)):
    file_path = os.path.join(DATA_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    retrain.retrain_model(file_path)
    return {"message": "Model retrained successfully"}

@app.get("/evaluate/")
async def trigger_evaluation():
    evaluate.evaluate_model()
    return {"message": "Model evaluated successfully"}

@app.post("/monitor/")
async def monitor_accuracy(input: MonitorInput):
    should_retrain = monitor.check_accuracy_threshold(input.threshold)
    if should_retrain:
        retrain.retrain_model(os.path.join(DATA_DIR, "new_data.csv"))
        return {"message": "Accuracy below threshold. Model retrained."}
    return {"message": "Accuracy above threshold. No retraining needed."}
