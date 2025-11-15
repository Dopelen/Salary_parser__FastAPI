from typing import List
from sqlalchemy import insert, select, func
from databases import Database
from app.models.vacancy import Vacancy
from app.database.tables import vacancies_table

async def insert_vacancies(database: Database, vacancies: List[Vacancy]):
    """Вставка вакансий в БД, игнорируя дубликаты по PRIMARY KEY."""
    if not vacancies:
        return

    query = insert(vacancies_table).prefix_with("IGNORE")
    values = [
        {
            "id": vac.id,
            "name": vac.name,
            "employer": vac.employer,
            "salary_from": vac.salary_from,
            "salary_to": vac.salary_to,
            "salary_currency": vac.salary_currency,
            "average_salary": vac.average_salary,
        }
        for vac in vacancies
    ]
    await database.execute_many(query=query, values=values)


async def get_salary_aggregates(database: Database):
    """Получение агрегированных данных по зарплатам."""
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
    return result