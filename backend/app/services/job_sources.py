from dataclasses import dataclass
from typing import Any

import httpx

from app.config import get_settings
from app.utils.logging import logger

settings = get_settings()


@dataclass
class RawJob:
    company: str
    role: str
    location: str
    salary: str | None
    apply_link: str
    description: str
    source: str
    raw_payload: dict[str, Any]


class JobSearchService:
    async def search_india_jobs(self, analysis: dict) -> list[RawJob]:
        target_roles = analysis.get("target_roles") or ["software engineer", "analyst"]
        results: list[RawJob] = []
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds, follow_redirects=True) as client:
            for role in target_roles[:4]:
                results.extend(await self._search_adzuna(client, role))
            results.extend(await self._search_greenhouse(client))
            results.extend(await self._search_lever(client))
            results.extend(await self._search_wellfound())
        unique: dict[str, RawJob] = {}
        for job in results:
            if self._is_india_job(job):
                unique[f"{job.company.lower()}:{job.role.lower()}:{job.apply_link}"] = job
        return list(unique.values())[:75]

    async def _search_adzuna(self, client: httpx.AsyncClient, role: str) -> list[RawJob]:
        if not settings.adzuna_app_id or not settings.adzuna_app_key:
            return []
        try:
            response = await client.get(
                "https://api.adzuna.com/v1/api/jobs/in/search/1",
                params={
                    "app_id": settings.adzuna_app_id,
                    "app_key": settings.adzuna_app_key,
                    "results_per_page": 20,
                    "what": role,
                    "where": "India",
                    "content-type": "application/json",
                },
            )
            response.raise_for_status()
            return [
                RawJob(
                    company=item.get("company", {}).get("display_name", "Unknown"),
                    role=item.get("title", "Unknown role"),
                    location=item.get("location", {}).get("display_name", "India"),
                    salary=self._salary(item.get("salary_min"), item.get("salary_max")),
                    apply_link=item.get("redirect_url", ""),
                    description=item.get("description", ""),
                    source="adzuna",
                    raw_payload=item,
                )
                for item in response.json().get("results", [])
            ]
        except Exception as exc:
            logger.warning("adzuna_search_failed", error=str(exc), role=role)
            return []

    async def _search_greenhouse(self, client: httpx.AsyncClient) -> list[RawJob]:
        jobs: list[RawJob] = []
        for company in settings.greenhouse_company_list:
            try:
                response = await client.get(f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs", params={"content": "true"})
                if response.status_code == 404:
                    continue
                response.raise_for_status()
                for item in response.json().get("jobs", []):
                    jobs.append(
                        RawJob(
                            company=company.title(),
                            role=item.get("title", "Unknown role"),
                            location=item.get("location", {}).get("name", "India"),
                            salary=None,
                            apply_link=item.get("absolute_url", ""),
                            description=item.get("content", ""),
                            source="greenhouse",
                            raw_payload=item,
                        )
                    )
            except Exception as exc:
                logger.warning("greenhouse_search_failed", error=str(exc), company=company)
        return jobs

    async def _search_wellfound(self) -> list[RawJob]:
        logger.info("wellfound_search_skipped", reason="No stable public jobs API; configure a licensed feed before enabling.")
        return []

    async def _search_lever(self, client: httpx.AsyncClient) -> list[RawJob]:
        jobs: list[RawJob] = []
        for company in settings.lever_company_list:
            try:
                response = await client.get(f"https://api.lever.co/v0/postings/{company}", params={"mode": "json"})
                if response.status_code == 404:
                    continue
                response.raise_for_status()
                for item in response.json():
                    categories = item.get("categories") or {}
                    jobs.append(
                        RawJob(
                            company=company.title(),
                            role=item.get("text", "Unknown role"),
                            location=categories.get("location", "India"),
                            salary=None,
                            apply_link=item.get("hostedUrl", ""),
                            description=item.get("descriptionPlain", "") or item.get("description", ""),
                            source="lever",
                            raw_payload=item,
                        )
                    )
            except Exception as exc:
                logger.warning("lever_search_failed", error=str(exc), company=company)
        return jobs

    def _is_india_job(self, job: RawJob) -> bool:
        text = f"{job.location} {job.description}".lower()
        india_terms = ["india", "bangalore", "bengaluru", "mumbai", "pune", "delhi", "gurgaon", "gurugram", "hyderabad", "chennai", "noida", "remote - india"]
        return any(term in text for term in india_terms)

    def _salary(self, minimum: float | None, maximum: float | None) -> str | None:
        if not minimum and not maximum:
            return None
        return f"{int(minimum or 0):,} - {int(maximum or 0):,} INR"
