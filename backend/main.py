from fastapi import FastAPI
app = FastAPI(title="RepoPilot API")
@app.get("/")
def home():
    return {"message": "Welcome to RepoPilot", "status": "running"}
@app.get("/health")
def health_check():
    return {"status": "healthy"}
