import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database.session import get_db
from app.models.schemas import AnalyzeResponse, HealthResponse
from app.services.pipeline import AnalysisPipeline
from app.services.resume_input import download_pdf, read_upload, save_temp_pdf
from app.utils.security import validate_pdf_upload

router = APIRouter()
settings = get_settings()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name)


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    email: EmailStr = Form(...),
    github_url: str | None = Form(None),
    resume_pdf: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
) -> AnalyzeResponse:
    if not resume_pdf and not github_url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide either a resume PDF or a GitHub URL.")
    if resume_pdf and github_url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide only one resume source.")

    source_type = "upload"
    source_url = None
    temp_id = str(uuid.uuid4())
    if resume_pdf:
        validate_pdf_upload(resume_pdf)
        pdf_content = await read_upload(resume_pdf)
        temp_path = save_temp_pdf(pdf_content, temp_id)
    else:
        source_type = "github"
        source_url = github_url
        pdf_content = await download_pdf(github_url or "")
        temp_path = save_temp_pdf(pdf_content, temp_id)

    return await AnalysisPipeline().run(temp_path, email=str(email), source_type=source_type, db=db, source_url=source_url)
