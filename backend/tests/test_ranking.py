from app.services.job_sources import RawJob
from app.services.ranking import JobRanker


def test_ranker_scores_and_categories_jobs():
    analysis = {
        "skills": ["python", "sql", "fastapi"],
        "target_roles": ["Backend Engineer"],
        "ats_score": 80,
    }
    jobs = [
        RawJob(
            company="Acme",
            role="Backend Engineer",
            location="Bengaluru, India",
            salary=None,
            apply_link="https://example.com/job",
            description="Python FastAPI SQL role requiring 3+ years of backend experience.",
            source="test",
            raw_payload={},
        )
    ]

    ranked = JobRanker().rank("Python SQL FastAPI backend APIs", analysis, jobs)

    assert ranked[0].company == "Acme"
    assert ranked[0].fit_score > 70
    assert ranked[0].category in {"High Probability", "Medium Probability"}
