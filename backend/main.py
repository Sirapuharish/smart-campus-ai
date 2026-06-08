from fastapi import FastAPI

app = FastAPI(title="SmartCampus API")

@app.get("/")
def home():
    return {"message": "SmartCampus API Running"}
from fastapi import FastAPI

app = FastAPI(title="SmartCampus API")

@app.get("/")
def home():
    return {"message": "SmartCampus API Running"}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "project": "SmartCampus"
    }

@app.get("/student")
def student():
    return {
        "name": "Harish",
        "role": "Student"
    }