import json

import gspread
from google.oauth2.service_account import Credentials

from app.config import get_settings
from app.models.schemas import JobMatch
from app.utils.logging import logger

settings = get_settings()


class GoogleSheetsService:
    def upload(self, jobs: list[JobMatch], resume_id: str) -> str | None:
        if not settings.google_service_account_json:
            logger.warning("google_sheets_skipped", reason="GOOGLE_SERVICE_ACCOUNT_JSON missing")
            return None
        credentials_info = json.loads(settings.google_service_account_json)
        credentials = Credentials.from_service_account_info(
            credentials_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"],
        )
        client = gspread.authorize(credentials)
        spreadsheet = client.create(f"AI Job Tracker {resume_id}")
        worksheet = spreadsheet.sheet1
        worksheet.update(
            [list(self._row(jobs[0]).keys())] + [list(self._row(job).values()) for job in jobs] if jobs else [["No jobs found"]],
            value_input_option="USER_ENTERED",
        )
        spreadsheet.share(None, perm_type="anyone", role="reader")
        return spreadsheet.url

    def _row(self, job: JobMatch) -> dict:
        return {
            "Company": job.company,
            "Role": job.role,
            "Location": job.location,
            "Salary": job.salary,
            "Fit Score": job.fit_score,
            "Category": job.category,
            "Apply Link": job.apply_link,
            "Why Match": job.why_match,
        }
