from fastapi import FastAPI
from data.consultants import CONSULTANTS_DATA

app = FastAPI(title="Konsulent API", version="1.0.0")

@app.get("/")
async def root():
  return {"message": "Hello from Konsulent API"}

@app.get("/konsulenter")
async def get_consultants() -> list[dict]:
  """
  Return a list of all consultants
  """
  return CONSULTANTS_DATA