from pydantic import BaseModel, model_validator
from typing import Optional

class Vacancy(BaseModel):
    id: str
    name: str
    employer: Optional[str]
    salary_from: Optional[int]
    salary_to: Optional[int]
    salary_currency: Optional[str]
    average_salary: Optional[int] = None

    @model_validator(mode="after")
    def calculate_average_salary(cls, values):
        salary_from = values.salary_from
        salary_to = values.salary_to
        currency = values.salary_currency

        # высчитываем только если валюта RUR (не используется RUB по какой-то причине) и есть хотя бы одно значение
        if currency == "RUR" and (salary_from or salary_to):
            if salary_from and salary_to:
                values.average_salary = (salary_from + salary_to) // 2
            else:
                values.average_salary = salary_from or salary_to
        return values