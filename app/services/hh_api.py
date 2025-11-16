import httpx
from app.models.vacancy import Vacancy
from typing import List

async def fetch_vacancies(query: str, per_page: int) -> List[Vacancy]:
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": query,
        "search_field": "name",
        "per_page": per_page,
        "page": 0,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    result = []
    for item in data.get("items", []):
        salary = item.get("salary")
        vac = Vacancy(
            id=item.get("id"),
            name=item.get("name"),
            employer=item.get("employer", {}).get("name"),
            salary_from=salary.get("from") if salary else None,
            salary_to=salary.get("to") if salary else None,
            salary_currency=salary.get("currency") if salary else None,
        )
        result.append(vac)
    return result