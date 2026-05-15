from pathlib import Path

import httpx
from fastapi import HTTPException, UploadFile, status

from app.config import get_settings
from app.utils.security import validate_download_url

settings = get_settings()


def github_to_raw_url(url: str) -> str:
    if "github.com" in url and "/blob/" in url:
        return url.replace("https://github.com/", "https://raw.githubusercontent.com/").replace("/blob/", "/")
    return url


async def read_upload(file: UploadFile) -> bytes:
    content = await file.read()
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Resume PDF is too large.")
    if not content.startswith(b"%PDF"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is not a valid PDF.")
    return content


async def download_pdf(url: str) -> bytes:
    raw_url = github_to_raw_url(url)
    validate_download_url(raw_url)
    async with httpx.AsyncClient(timeout=settings.request_timeout_seconds, follow_redirects=True) as client:
        response = await client.get(raw_url)
        response.raise_for_status()
    content = response.content
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Remote PDF is too large.")
    if not content.startswith(b"%PDF"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Remote file is not a valid PDF.")
    return content


def save_temp_pdf(content: bytes, resume_id: str) -> Path:
    output_dir = Path("/tmp/resume-job-hunter")
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{resume_id}.pdf"
    path.write_bytes(content)
    return path
