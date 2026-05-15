import json
from pathlib import Path

from openai import AsyncOpenAI

from app.config import get_settings

settings = get_settings()


class OpenAIAnalyzer:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.prompt = Path(__file__).resolve().parents[1].joinpath("prompts", "resume_analysis.txt").read_text(encoding="utf-8")

    async def analyze(self, resume_text: str) -> dict:
        if not self.client:
            return self._fallback_analysis(resume_text)

        response = await self.client.responses.create(
            model=settings.openai_model,
            input=[
                {"role": "system", "content": "You are a precise recruiting analyst. Return valid JSON only."},
                {"role": "user", "content": f"{self.prompt}\n\nResume text:\n{resume_text[:18000]}"},
            ],
            text={"format": {"type": "json_object"}},
        )
        return json.loads(response.output_text)

    def _fallback_analysis(self, resume_text: str) -> dict:
        lowered = resume_text.lower()
        skill_candidates = [
            "python",
            "sql",
            "fastapi",
            "react",
            "aws",
            "docker",
            "analytics",
            "machine learning",
            "product",
            "stakeholder",
        ]
        skills = [skill for skill in skill_candidates if skill in lowered]
        return {
            "target_roles": ["Software Engineer", "Backend Engineer", "Data Analyst", "Product Analyst"],
            "skills": skills or ["python", "sql", "communication"],
            "seniority": "Associate/Mid-level, 3-5 years",
            "industries": ["Technology", "SaaS", "Consulting", "Fintech"],
            "keywords": skills or ["python", "sql", "api", "analytics"],
            "ats_score": 72,
            "summary": "Fallback analysis generated because OPENAI_API_KEY is not configured.",
        }
