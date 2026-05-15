from urllib.parse import urlparse

from fastapi import HTTPException, UploadFile, status

from app.config import get_settings

settings = get_settings()


def validate_pdf_upload(file: UploadFile) -> None:
    if file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF uploads are allowed.")
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file must end with .pdf.")


def validate_download_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume URL must use HTTPS.")
    if parsed.hostname not in {"github.com", "raw.githubusercontent.com"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only GitHub resume PDF URLs are supported.")
    if not parsed.path.lower().endswith(".pdf"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume URL must point to a PDF.")
