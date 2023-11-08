from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config.environment import env_data

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{env_data.db_user}:{env_data.db_pass}@{env_data.db_host}:{env_data.db_port}/{env_data.db_name}"

Engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=env_data.debug, future=True)


AsyncSessionFactory = async_sessionmaker(
    Engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncSession:
    async with AsyncSession(Engine) as session:
        yield session
