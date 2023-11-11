import os
import shutil
from typing import List

from fastapi import APIRouter
from fastapi import File, UploadFile

router = APIRouter()


@router.post("/uploadfiles")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        file_path = os.path.join("./data/uploaded_files", file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    return {"file_names": [file.filename for file in files]}
