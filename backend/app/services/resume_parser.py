from pathlib import Path

import pdfplumber
from fastapi import HTTPException, status


def extract_resume_text(path: Path) -> str:
    try:
        parts: list[str] = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text(x_tolerance=1, y_tolerance=3) or ""
                if text.strip():
                    parts.append(text.strip())
        clean_text = "\n\n".join(parts)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Could not parse resume PDF.") from exc

    if len(clean_text) < 100:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Resume text is too short to analyze.")
    return clean_text
