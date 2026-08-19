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
            query += " WHERE " + " AND ".join(f"{k}='{v}'" for k, v in where)
        return query

    @staticmethod
    def insert(table, data):
        cols = ", ".join(k for k, _ in data)
        vals = ", ".join(f"'{v}'" for _, v in data)
        return f"INSERT INTO {table} ({cols}) VALUES ({vals})"

    @staticmethod
    def delete_(table, where=None):
        if where is None:
            where = []
        query = "DELETE FROM " + table
        if where:
            query += " WHERE " + " AND ".join(f"{k}='{v}'" for k, v in where)
        return query

    @staticmethod
    def update(table, data, where=None):
        if where is None:
            where = []
        query = f"UPDATE {table} SET " + ", ".join(f"{k}='{v}'" for k, v in data)
        if where:
            query += " WHERE " + " AND ".join(f"{k}='{v}'" for k, v in where)
        return query