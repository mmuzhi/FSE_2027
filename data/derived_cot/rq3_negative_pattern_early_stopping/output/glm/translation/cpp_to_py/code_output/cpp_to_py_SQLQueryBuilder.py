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

        query += f" FROM {table}"

        if where:
            conditions = " AND ".join(f"{key}='{value}'" for key, value in where)
            query += f" WHERE {conditions}"

        return query

    @staticmethod
    def insert(table, data):
        columns = ", ".join(key for key, value in data)
        values = ", ".join(f"'{value}'" for key, value in data)
        return f"INSERT INTO {table} ({columns}) VALUES ({values})"

    @staticmethod
    def delete_(table, where=None):
        if where is None:
            where = []

        query = f"DELETE FROM {table}"

        if where:
            conditions = " AND ".join(f"{key}='{value}'" for key, value in where)
            query += f" WHERE {conditions}"

        return query

    @staticmethod
    def update(table, data, where=None):
        if where is None:
            where = []

        set_clause = ", ".join(f"{key}='{value}'" for key, value in data)
        query = f"UPDATE {table} SET {set_clause}"

        if where:
            conditions = " AND ".join(f"{key}='{value}'" for key, value in where)
            query += f" WHERE {conditions}"

        return query