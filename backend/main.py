from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import io
import zipfile
from zip_safety import find_unsafe_names
app = FastAPI(title="RepoPilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to RepoPilot", "status": "running"}
@app.get("/health")
def health_check():
    return {"status": "healthy"}
MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB


@app.post("/api/projects")
async def upload_project(file: UploadFile):
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip files are allowed")

    contents = await file.read(MAX_UPLOAD_BYTES + 1)

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="The file is empty")
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File too large (max 10 MB)")
    try:
        with zipfile.ZipFile(io.BytesIO(contents)) as zf:
            names = zf.namelist()
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Not a valid ZIP file")

    if find_unsafe_names(names):
        raise HTTPException(status_code=400, detail="ZIP contains unsafe file paths")

    return {"filename": file.filename, "size_bytes": len(contents)}