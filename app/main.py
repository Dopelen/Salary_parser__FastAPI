from fastapi import FastAPI
from app.database.database import init_models, database
from app.routers import vacancies_router

app = FastAPI(title="Vacancies API")
app.include_router(vacancies_router.router, prefix="/vacancies")

@app.on_event("startup")
async def startup():
    await init_models()
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": "API is working"}