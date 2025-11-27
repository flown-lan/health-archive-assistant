from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(title="Health Archive Assistant Backend")

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Health Archive Assistant API is running"}
