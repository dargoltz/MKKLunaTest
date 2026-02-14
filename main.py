from fastapi import FastAPI
from src.core import lifespan

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async  def health():
    return {"status": "ok"}
