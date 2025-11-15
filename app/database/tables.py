from app.database.database import metadata
import sqlalchemy

vacancies_table = sqlalchemy.Table(
    "vacancies",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(255), primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(255)),
    sqlalchemy.Column("employer", sqlalchemy.String(255)),
    sqlalchemy.Column("salary_from", sqlalchemy.Integer),
    sqlalchemy.Column("salary_to", sqlalchemy.Integer),
    sqlalchemy.Column("salary_currency", sqlalchemy.String(10)),
    sqlalchemy.Column("average_salary", sqlalchemy.Integer),
)

