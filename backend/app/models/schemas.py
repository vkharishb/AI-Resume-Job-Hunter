from pydantic import BaseModel, EmailStr, HttpUrl


class JobMatch(BaseModel):
    company: str
    role: str
    location: str
    salary: str | None = None
    fit_score: float
    category: str
    apply_link: str
    why_match: str


class AnalyzeResponse(BaseModel):
    resume_id: str
    google_sheet_url: str | None
    excel_file: str
    jobs: list[JobMatch]
    analysis_summary: dict


class GitHubAnalyzeRequest(BaseModel):
    github_url: HttpUrl
    email: EmailStr


class HealthResponse(BaseModel):
    status: str
    service: str
