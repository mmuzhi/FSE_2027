from typing import List, Tuple


class SQLQueryBuilder:
    @staticmethod
    def select(
        table: str,
        columns: List[str] = None,
        where: List[Tuple[str, str]] = None
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
            conditions = [f"{key}='{value}'" for key, value in where]
            query += " WHERE " + " AND ".join(conditions)

        return query

    @staticmethod
    def insert(
        table: str,
        data: List[Tuple[str, str]]
    ) -> str:
        if not data:
            return ""  # or raise? C++ code doesn't handle empty, but we keep same: will produce "INSERT INTO table () VALUES ()"
        keys = [pair[0] for pair in data]
        values = [f"'{pair[1]}'" for pair in data]
        query = f"INSERT INTO {table} ({', '.join(keys)}) VALUES ({', '.join(values)})"
        return query

    @staticmethod
    def delete_(
        table: str,
        where: List[Tuple[str, str]] = None
    ) -> str:
        if where is None:
            where = []
        query = "DELETE FROM " + table
        if where:
            conditions = [f"{key}='{value}'" for key, value in where]
            query += " WHERE " + " AND ".join(conditions)
        return query

    @staticmethod
    def update(
        table: str,
        data: List[Tuple[str, str]],
        where: List[Tuple[str, str]] = None
    ) -> str:
        if where is None:
            where = []
        set_clauses = [f"{key}='{value}'" for key, value in data]
        query = "UPDATE " + table + " SET " + ", ".join(set_clauses)
        if where:
            conditions = [f"{key}='{value}'" for key, value in where]
            query += " WHERE " + " AND ".join(conditions)
        return query