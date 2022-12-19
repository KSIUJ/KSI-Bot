import pathlib
import aiosqlite
import aiofiles

from typing import Any, Iterable, List


class DatabaseHandler:
    def __init__(self, db_path: str, build_path: str) -> None:
        self.db_path: str = db_path
        self.build_path: str = build_path

    async def build(self) -> None:
        """Build the database from schema file if it exists"""

        async with aiosqlite.connect(self.db_path) as db:
            if pathlib.Path(self.build_path).exists():
                await self.execute_file(self.build_path)
            else:
                raise FileNotFoundError(f"Database schema file doesn't exist {self.build_path}")
            await db.commit()

    async def commit(self) -> None:
        """Commit to the database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.commit()

    async def field(self, command, *values) -> Any:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.cursor()
            await cursor.execute(command, values)

            if (fetch := await cursor.fetchone()) is not None:
                return fetch[0]

    async def record(self, command, *values) -> Any | aiosqlite.Row | None:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.cursor()
            await cursor.execute(command, values)

            return cursor.fetchone()

    async def records(self, command, *values) -> Iterable[aiosqlite.Row]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.cursor()
            await cursor.execute(command, values)

            return await cursor.fetchall()

    async def column(self, command, *values) -> List[Any | aiosqlite.Row | None]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.cursor()
            await cursor.execute(command, values)

            return [row[0] for row in await cursor.fetchall()]

    async def execute(self, command, *values) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.cursor()
            await cursor.execute(command, values)

    async def execute_and_commit(self, command, *values) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.cursor()
            await cursor.execute(command, values)
            await db.commit()

    async def execute_file(self, path: str) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.cursor()
            async with aiofiles.open(path, mode="r", encoding="UTF-8") as script:
                await cursor.executescript(await script.read())
