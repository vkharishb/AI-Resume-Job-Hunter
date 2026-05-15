from pathlib import Path

import pandas as pd

from app.models.schemas import JobMatch


class ExcelService:
    def generate(self, jobs: list[JobMatch], resume_id: str) -> Path:
        output_dir = Path("/tmp/resume-job-hunter")
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"jobs-{resume_id}.xlsx"
        df = pd.DataFrame([job.model_dump() for job in jobs])
        df = df.rename(
            columns={
                "company": "Company",
                "role": "Role",
                "location": "Location",
                "salary": "Salary",
                "fit_score": "Fit Score",
                "category": "Category",
                "apply_link": "Apply Link",
                "why_match": "Why Match",
            }
        )
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Matched Jobs")
            worksheet = writer.sheets["Matched Jobs"]
            widths = {"A": 24, "B": 36, "C": 24, "D": 18, "E": 12, "F": 20, "G": 48, "H": 72}
            for column, width in widths.items():
                worksheet.column_dimensions[column].width = width
        return path
