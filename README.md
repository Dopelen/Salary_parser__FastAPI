# Vacancies API

API для работы с вакансиями: запрос вакансий с сайта, сохранение в базу данных MySQL и получение агрегированных данных о зарплатах.

## Содержание

- [Технологии](#технологии)
- [Установка](#установка)
- [Настройка базы данных](#настройка-базы-данных)
- [Запуск приложения](#запуск-приложения)
- [API эндпоинты](#api-эндпоинты)
- [Автоматический сбор вакансий](#автоматический-сбор-вакансий)
- [Примечания](#примечания)

## Технологии

- **Python 3.11**
- **FastAPI**
- **SQLAlchemy**
- **Databases** (асинхронная работа с базой)
- **MySQL 8.0**
- **APScheduler** (для планирования задач)
- **httpx** (для запросов вакансий)
- **Pydantic**
- **Poetry** (управление зависимостями)

## Установка

1. Клонировать репозиторий:

```bash
git clone https://github.com/Dopelen/Salary_parser__FastAPI.git
cd Salary_parser__FastAPI
```

2. Создать виртуальное окружение и установить зависимости через Poetry:

```bash
poetry install
poetry shell
```

## Настройка базы данных
1. Установить MySQL 8.0 (локально или на сервере).
2. Создать пользователя и базу данных:
```sql
CREATE DATABASE dbname CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON dbname.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
```
3. При необходимости Обновить "DATABASE_URL" в app/database/database.py:
```python
DATABASE_URL = "mysql+aiomysql://user:password@localhost/dbname"
```

## Запуск приложения
```bash
poetry run uvicorn app.main:app --reload
```

- Приложение будет доступно по адресу: http://127.0.0.1:8000
- Swagger UI с документацией: http://127.0.0.1:8000/docs


## API эндпоинты

1. Добавить вакансии в базу
```
POST /vacancies/db/add-vacancies
```
Параметры запроса:

*query* — текст поискового запроса для вакансий (по умолчанию: "Python разработчик")

*per_page* — количество вакансий на страницу (по умолчанию: 100, от 1 до 100)

Ответ:
```json
{
  "message": "Вакансии добавлены"
}
```

2. Получить все вакансии

```
GET /vacancies/db/vacancies
```

Ответ — список вакансий в формате модели Vacancy

3. Получить агрегированные данные по зарплатам

```GET /vacancies/db/salary-aggregates```
Ответ - результат обработки вакансий в базе
```json
{
  "vacancy_count": 150,
  "avg_salary": 120000,
  "min_salary": 50000,
  "max_salary": 250000
}
```

## Автоматический сбор вакансий
Приложение использует **APScheduler** для периодического вызова функции add_vacancies_to_db.

По умолчанию запуск планировщика выполняется при старте приложения.

Вы можете настроить интервал запуска задач в файле ```app/scheduler/scheduler_file.py```. 

Например, для ежечасного запуска: 
```scheduler.add_job(add_vacancies_to_db, "interval", hours=1)```


## Примечания
- Дубликаты вакансий игнорируются при вставке в базу.
- Все запросы к базе выполняются асинхронно.
- Таблицы создаются автоматически при старте приложения.