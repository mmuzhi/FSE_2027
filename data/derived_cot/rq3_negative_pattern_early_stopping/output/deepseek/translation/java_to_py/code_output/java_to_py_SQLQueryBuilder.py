import re


class SQLQueryBuilder:
    @staticmethod
    def select(table, columns, where=None):
        if isinstance(columns, str):
            if columns is None:
                columns = "*"
            columns = re.split(r',\s*', columns)
        elif columns is None:
            columns = ["*"]

        if len(columns) == 0:
            columns = ["*"]

        query = "SELECT " + (", ".join(columns) if columns else "*") + " FROM " + table
        if where:
            query += " WHERE " + " AND ".join(f"{k}='{v}'" for k, v in where.items())
        return query

    @staticmethod
    def insert(table, data):
        keys = list(data.keys())
        values = list(data.values())
        cols = ", ".join(keys)
        vals = ", ".join(f"'{v}'" for v in values)
        return f"INSERT INTO {table} ({cols}) VALUES ({vals})"

    @staticmethod
    def delete(table, where):
        query = "DELETE FROM " + table
        if where:
            query += " WHERE " + " AND ".join(f"{k}='{v}'" for k, v in where.items())
        return query

    @staticmethod
    def update(table, data, where):
        set_clause = ", ".join(f"{k}='{v}'" for k, v in data.items())
        query = f"UPDATE {table} SET {set_clause}"
        if where:
            query += " WHERE " + " AND ".join(f"{k}='{v}'" for k, v in where.items())
        return query