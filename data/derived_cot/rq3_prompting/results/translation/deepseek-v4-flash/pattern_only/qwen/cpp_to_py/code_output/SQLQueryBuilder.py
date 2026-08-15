class SQLQueryBuilder:
    @staticmethod
    def select(table, columns=None, where=None):
        if columns is None:
            columns = ["*"]
        if where is None:
            where = []

        parts = []
        if len(columns) == 1 and columns[0] == "*":
            parts.append("SELECT *")
        else:
            parts.append("SELECT ")
            parts.append(", ".join(columns))

        parts.append(" FROM " + table)

        if where:
            parts.append(" WHERE ")
            parts.append(" AND ".join(f"{k}='{v}'" for k, v in where))

        return "".join(parts)

    @staticmethod
    def insert(table, data):
        parts = []
        parts.append("INSERT INTO " + table + " (")
        parts.append(", ".join(k for k, v in data))
        parts.append(") VALUES (")
        parts.append(", ".join(f"'{v}'" for k, v in data))
        parts.append(")")
        return "".join(parts)

    @staticmethod
    def delete_(table, where=None):
        if where is None:
            where = []

        parts = ["DELETE FROM " + table]

        if where:
            parts.append(" WHERE ")
            parts.append(" AND ".join(f"{k}='{v}'" for k, v in where))

        return "".join(parts)

    @staticmethod
    def update(table, data, where=None):
        if where is None:
            where = []

        parts = ["UPDATE " + table + " SET "]
        parts.append(", ".join(f"{k}='{v}'" for k, v in data))

        if where:
            parts.append(" WHERE ")
            parts.append(" AND ".join(f"{k}='{v}'" for k, v in where))

        return "".join(parts)