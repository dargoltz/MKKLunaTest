from fastapi import FastAPI
from src.core import lifespan, VerifiedRequest

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async  def health(_: VerifiedRequest):
    return {"status": "ok"}
