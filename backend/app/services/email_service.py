from email.message import EmailMessage
from pathlib import Path
import smtplib

from app.config import get_settings
from app.utils.logging import logger

settings = get_settings()


class EmailService:
    def send_tracker(self, recipient: str, excel_path: Path) -> None:
        if not settings.smtp_username or not settings.smtp_password:
            logger.warning("email_skipped", reason="SMTP credentials missing", recipient=recipient)
            return
        message = EmailMessage()
        message["Subject"] = "Apply for the jobs"
        message["From"] = settings.smtp_from_email or settings.smtp_username
        message["To"] = recipient
        message.set_content("Attached is your AI-generated job application tracker.")
        message.add_attachment(
            excel_path.read_bytes(),
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="jobs.xlsx",
        )
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
            smtp.starttls()
            smtp.login(settings.smtp_username, settings.smtp_password)
            smtp.send_message(message)
