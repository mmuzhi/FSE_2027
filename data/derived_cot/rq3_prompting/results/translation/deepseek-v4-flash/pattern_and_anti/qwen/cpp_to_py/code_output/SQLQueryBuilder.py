class SQLQueryBuilder:
    @staticmethod
    def select(table, columns=None, where=None):
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
    def insert(table, data):
        columns = ", ".join(key for key, _ in data)
        values = ", ".join(f"'{value}'" for _, value in data)
        return f"INSERT INTO {table} ({columns}) VALUES ({values})"

    @staticmethod
    def delete_(table, where=None):
        if where is None:
            where = []

        query = "DELETE FROM " + table

        if where:
            query += " WHERE " + " AND ".join(
                f"{key}='{value}'" for key, value in where
            )

        return query

    @staticmethod
    def update(table, data, where=None):
        if where is None:
            where = []

        query = "UPDATE " + table + " SET " + ", ".join(
            f"{key}='{value}'" for key, value in data
        )

        if where:
            query += " WHERE " + " AND ".join(
                f"{key}='{value}'" for key, value in where
            )

        return query