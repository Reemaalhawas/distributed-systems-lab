from fastapi import FastAPI
import os

app = FastAPI()

SERVER_ID = os.getenv("SERVER_ID", "unknown")


@app.get("/")
def root():
    return {
        "message": "Hello from backend server",
        "server_id": SERVER_ID
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "server_id": SERVER_ID
    }

 
