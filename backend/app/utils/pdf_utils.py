from pathlib import Path

from fastapi import UploadFile


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as buffer:
        while chunk := upload_file.file.read(1024 * 64):
            buffer.write(chunk)
