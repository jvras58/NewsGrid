from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from utils.settings import settings

engine = create_async_engine(settings.database_url, echo=settings.echo_sql)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
