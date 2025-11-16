from fastapi import FastAPI
from app.database.database import init_models, database
from app.routers import vacancies_router
from app.scheduler.scheduler_file import scheduler

app = FastAPI(title="Vacancies API")
app.include_router(vacancies_router.router, prefix="/vacancies")

@app.on_event("startup")
async def startup():
    await init_models()
    await database.connect()
    scheduler.start()

@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown()
    await database.disconnect()