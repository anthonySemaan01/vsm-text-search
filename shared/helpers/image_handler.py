import base64
import os
import shutil

from fastapi import UploadFile


def load_image(path: str):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            base64image = base64.b64encode(f.read())
            return base64image

    else:
        return None


def save_image(upload_file: UploadFile, destination: str) -> str:
    with open(destination, "wb+") as file_object:
        shutil.copyfileobj(upload_file.file, file_object)
    return destination