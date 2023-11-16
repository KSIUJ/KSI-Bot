import pathlib
import logging


from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)

from app.database.models.reminder import (
    Reminders,
)  # import needed for sqlalchemy to create the table
from app.database.models.base import Base

logger = logging.getLogger(__name__)


class DatabaseHandler:
    def __init__(self, database_path: str) -> None:
        self._engine: AsyncEngine = create_async_engine(
            f"sqlite+aiosqlite:///{database_path}", future=True, echo=True
        )

        self._session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self._engine, expire_on_commit=False
        )

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()

    @property
    def session(self) -> async_sessionmaker[AsyncSession]:
        return self._session


def create_database_directory(database_path: str) -> None:
    """Create the database directory if it doesn't exist.

    Args:
        database_path (str): The path to the database.
    """

    database_directory = pathlib.Path(database_path).parent
    pathlib.Path(database_directory).mkdir(parents=True, exist_ok=True)
