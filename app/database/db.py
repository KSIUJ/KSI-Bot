import pathlib
import sqlite3

from typing import Any, List


class DatabaseHandler:
    def __init__(self, db_path: str, build_path: str) -> None:
        self._db_path = db_path
        self._build_path = build_path
        self._connection = sqlite3.connect(db_path)
        self._cursor = self._connection.cursor()

    def build(self) -> None:
        if pathlib.Path(self._build_path).exists():
            self.execute_file(self._build_path)
        else:
            raise FileNotFoundError(
                f"Database schema file doesn't exist {self._build_path}"
            )
        self.commit()

    def commit(self) -> None:
        self._connection.commit()

    def close(self) -> None:
        self._connection.close()

    def field(self, command, *values) -> Any:
        self._cursor.execute(command, values)

        if (fetch := self._cursor.fetchone()) is not None:
            return fetch[0]

    def record(self, command, *values) -> Any:
        self._cursor.execute(command, values)

        return self._cursor.fetchone()

    def records(self, command, *values) -> List[Any]:
        self._cursor.execute(command, values)

        return self._cursor.fetchall()

    def column(self, command, *values) -> List[Any]:
        self._cursor.execute(command, values)

        return [row[0] for row in self._cursor.fetchall()]

    def execute(self, command, *values):
        self._cursor.execute(command, values)

    def execute_file(self, path: str) -> None:
        with open(path, "r", encoding="UTF-8") as script:
            self._cursor.executescript(script.read())
