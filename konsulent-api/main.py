from fastapi import FastAPI

app = FastAPI(title="Konsulent API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello from Konsulent API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}