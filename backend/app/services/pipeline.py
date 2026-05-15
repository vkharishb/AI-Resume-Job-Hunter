import uuid
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import JobHistory, ProcessingLog, ResumeMetadata
from app.models.schemas import AnalyzeResponse
from app.services.email_service import EmailService
from app.services.excel_service import ExcelService
from app.services.job_sources import JobSearchService
from app.services.openai_service import OpenAIAnalyzer
from app.services.ranking import JobRanker
from app.services.resume_parser import extract_resume_text
from app.services.sheets_service import GoogleSheetsService
from app.utils.logging import logger


class AnalysisPipeline:
    def __init__(self) -> None:
        self.openai = OpenAIAnalyzer()
        self.jobs = JobSearchService()
        self.ranker = JobRanker()
        self.excel = ExcelService()
        self.sheets = GoogleSheetsService()
        self.email = EmailService()

    async def run(self, pdf_path: Path, email: str, source_type: str, db: AsyncSession, source_url: str | None = None) -> AnalyzeResponse:
        resume_id = uuid.uuid4()
        metadata = ResumeMetadata(id=resume_id, source_type=source_type, source_url=source_url, email=email)
        db.add(metadata)
        await db.flush()
        try:
            await self._log(db, resume_id, "info", "Parsing resume", {})
            resume_text = extract_resume_text(pdf_path)
            metadata.text_length = len(resume_text)

            await self._log(db, resume_id, "info", "Analyzing resume with OpenAI", {})
            analysis = await self.openai.analyze(resume_text)
            metadata.analysis = analysis

            await self._log(db, resume_id, "info", "Searching live India jobs", {"sources": ["Adzuna", "Greenhouse", "Lever", "Wellfound placeholder"]})
            raw_jobs = await self.jobs.search_india_jobs(analysis)
            ranked_jobs = self.ranker.rank(resume_text, analysis, raw_jobs)

            excel_path = self.excel.generate(ranked_jobs, str(resume_id))
            sheet_url = self.sheets.upload(ranked_jobs, str(resume_id))
            metadata.google_sheet_url = sheet_url

            for job in ranked_jobs:
                db.add(
                    JobHistory(
                        resume_id=resume_id,
                        company=job.company,
                        role=job.role,
                        location=job.location,
                        salary=job.salary,
                        fit_score=job.fit_score,
                        category=job.category,
                        apply_link=job.apply_link,
                        why_match=job.why_match,
                        raw_payload=job.model_dump(),
                    )
                )
            await db.commit()
            self.email.send_tracker(email, excel_path)
            return AnalyzeResponse(
                resume_id=str(resume_id),
                google_sheet_url=sheet_url,
                excel_file=str(excel_path),
                jobs=ranked_jobs,
                analysis_summary=analysis,
            )
        except Exception as exc:
            await db.rollback()
            logger.exception("analysis_pipeline_failed", resume_id=str(resume_id), error=str(exc))
            raise

    async def _log(self, db: AsyncSession, resume_id: uuid.UUID, level: str, message: str, context: dict) -> None:
        db.add(ProcessingLog(resume_id=resume_id, level=level, message=message, context=context))
        await db.flush()
