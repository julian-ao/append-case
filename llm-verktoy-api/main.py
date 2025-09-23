from fastapi import FastAPI

app = FastAPI(title="LLM Verktøy API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello from LLM Verktøy API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}