from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.routers.vacancies_router import add_vacancies_to_db

scheduler = AsyncIOScheduler()

scheduler.add_job(
    add_vacancies_to_db,
    "interval",
    hours=1,
    kwargs={
        "query": "Python разработчик",
        "per_page": 100
    }
)