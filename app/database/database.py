from databases import Database
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "mysql+aiomysql://user:password@localhost/dbname"

database = Database(DATABASE_URL)

metadata = MetaData()

engine = create_async_engine(DATABASE_URL, echo=True)

async def init_models():
    """Создаёт таблицы, если их ещё нет"""
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)