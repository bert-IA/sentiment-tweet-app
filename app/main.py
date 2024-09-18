from fastapi import FastAPI
from pydantic import BaseModel
from app.model.model import predict_pipeline
from app.model.model import __version__ as model_version
import uvicorn
import os

app = FastAPI()


class TextIn(BaseModel):
    text: str

class PredictionOut(BaseModel):
    sentiment: str

@app.get("/")
def home():
    return {"health_check": "ok", "model_version": model_version}

@app.post("/predict", response_model=PredictionOut)
def predict(payload: TextIn):
    sentiment = predict_pipeline(payload.text)
    return {"sentiment": sentiment}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)