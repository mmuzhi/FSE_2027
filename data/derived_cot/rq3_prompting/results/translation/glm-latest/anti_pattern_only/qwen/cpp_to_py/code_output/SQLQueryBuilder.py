from typing import List, Optional, Tuple

Pair = Tuple[str, str]


class SQLQueryBuilder:
    @staticmethod
    def select(
        table: str,
        columns: Optional[List[str]] = None,
        where: Optional[List[Pair]] = None,
    ) -> str:
        if columns is None:
            columns = ["*"]
        if where is None:
            where = []

        if len(columns) == 1 and columns[0] == "*":
            query = "SELECT *"
        else:
            query = "SELECT " + ", ".join(columns)
        query += " FROM " + table
        if where:
            query += " WHERE " + " AND ".join(
                f"{key}='{value}'" for key, value in where
            )
        return query

    @staticmethod
    def insert(table: str, data: List[Pair]) -> str:
        query = "INSERT INTO " + table + " ("
        query += ", ".join(key for key, _ in data)
        query += ") VALUES ("
        query += ", ".join(f"'{value}'" for _, value in data)
        query += ")"
        return query

    @staticmethod
    def delete_(table: str, where: Optional[List[Pair]] = None) -> str:
        if where is None:
            where = []

        query = "DELETE FROM " + table
        if where:
            query += " WHERE " + " AND ".join(
                f"{key}='{value}'" for key, value in where
            )
        return query

    @staticmethod
    def update(
        table: str,
        data: List[Pair],
        where: Optional[List[Pair]] = None,
    ) -> str:
        if where is None:
            where = []

        query = "UPDATE " + table + " SET "
        query += ", ".join(f"{key}='{value}'" for key, value in data)
        if where:
            query += " WHERE " + " AND ".join(
                f"{key}='{value}'" for key, value in where
            )
        return query