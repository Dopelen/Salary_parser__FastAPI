from fastapi import APIRouter, Query
from typing import List
from sqlalchemy import select, func

from app.models.vacancy import Vacancy
from app.database.database import database
from app.database.tables import vacancies_table
from app.services.hh_api import fetch_vacancies
from app.database.db_operations import insert_vacancies

router = APIRouter()

@router.post("/db/add-vacancies")
async def add_vacancies_to_db(
    query: str = Query("Python разработчик"),
    per_page: int = Query(100, ge=1, le=100)
):
    vacancies = await fetch_vacancies(query, per_page)
    await insert_vacancies(database, vacancies)

    return {"message": "Вакансии добавлены"}


@router.get("/db/vacancies", response_model=List[Vacancy])
async def get_vacancies_from_db():
    query = select(vacancies_table)
    rows = await database.fetch_all(query)

    return [Vacancy(**row) for row in rows]


@router.get("/db/salary-aggregates")
async def get_salary_aggregates():
    query = (
        select(
            func.count(vacancies_table.c.id).label("vacancy_count"),
            func.avg(vacancies_table.c.average_salary).label("avg_salary"),
            func.min(vacancies_table.c.average_salary).label("min_salary"),
            func.max(vacancies_table.c.average_salary).label("max_salary"),
        )
        .where(vacancies_table.c.salary_currency == "RUR")
    )
    result = await database.fetch_one(query)
    return dict(result) if result else {}