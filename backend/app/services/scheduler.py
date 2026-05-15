from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import get_settings
from app.utils.logging import logger

settings = get_settings()


def start_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")

    async def refresh_job_sources() -> None:
        logger.info("daily_job_refresh_tick", note="Live searches are executed per analysis request; this tick is ready for cache warming.")

    scheduler.add_job(refresh_job_sources, "cron", hour=settings.daily_refresh_hour_utc, id="daily-job-refresh", replace_existing=True)
    scheduler.start()
    return scheduler
