import re

from app.models.schemas import JobMatch
from app.services.job_sources import RawJob


class JobRanker:
    def rank(self, resume_text: str, analysis: dict, jobs: list[RawJob]) -> list[JobMatch]:
        resume_words = self._tokens(resume_text)
        skills = {skill.lower() for skill in analysis.get("skills", [])}
        target_roles = {role.lower() for role in analysis.get("target_roles", [])}
        ats_score = float(analysis.get("ats_score") or 70)

        ranked: list[JobMatch] = []
        for job in jobs:
            description_words = self._tokens(f"{job.role} {job.description}")
            keyword_match = self._overlap(resume_words, description_words)
            skill_overlap = self._skill_overlap(skills, job)
            role_relevance = max((self._text_similarity(role, job.role.lower()) for role in target_roles), default=0.35)
            experience_overlap = self._experience_score(job.description)
            score = min(
                100.0,
                (keyword_match * 30) + (skill_overlap * 25) + (experience_overlap * 15) + ((ats_score / 100) * 15) + (role_relevance * 15),
            )
            category = "High Probability" if score >= 78 else "Medium Probability" if score >= 58 else "Stretch Roles"
            ranked.append(
                JobMatch(
                    company=job.company,
                    role=job.role,
                    location=job.location,
                    salary=job.salary or "Not disclosed",
                    fit_score=round(score, 1),
                    category=category,
                    apply_link=job.apply_link,
                    why_match=self._why_match(skills, job, score),
                )
            )
        return sorted(ranked, key=lambda item: item.fit_score, reverse=True)[:30]

    def _tokens(self, text: str) -> set[str]:
        return {token for token in re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}", text.lower()) if len(token) > 2}

    def _overlap(self, left: set[str], right: set[str]) -> float:
        if not left or not right:
            return 0.0
        return min(1.0, len(left & right) / max(12, len(right) * 0.15))

    def _skill_overlap(self, skills: set[str], job: RawJob) -> float:
        if not skills:
            return 0.45
        text = f"{job.role} {job.description}".lower()
        return len([skill for skill in skills if skill in text]) / len(skills)

    def _text_similarity(self, role: str, title: str) -> float:
        role_tokens = self._tokens(role)
        title_tokens = self._tokens(title)
        return self._overlap(role_tokens, title_tokens)

    def _experience_score(self, description: str) -> float:
        text = description.lower()
        if any(term in text for term in ["3+ years", "4+ years", "5+ years", "3 years", "4 years", "5 years"]):
            return 1.0
        if any(term in text for term in ["2+ years", "6+ years", "associate", "mid"]):
            return 0.75
        return 0.5

    def _why_match(self, skills: set[str], job: RawJob, score: float) -> str:
        matched = [skill for skill in sorted(skills) if skill in f"{job.role} {job.description}".lower()][:5]
        skill_text = ", ".join(matched) if matched else "transferable resume keywords"
        return f"Fit score {score:.1f}/100 based on role relevance, ATS strength, experience signals, and overlap with {skill_text}."
