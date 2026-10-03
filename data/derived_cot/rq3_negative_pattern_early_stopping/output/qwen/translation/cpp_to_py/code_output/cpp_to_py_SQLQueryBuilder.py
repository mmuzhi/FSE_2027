class SQLQueryBuilder:

    @staticmethod
    def select(table, columns=None, where=None):
        if columns is None:
            columns = ['*']
        if where is None:
            where = []
        parts = []
        if columns == ['*']:
            parts.append("SELECT *")
        else:
            parts.append("SELECT " + ", ".join(columns))
        parts.append("FROM " + table)
        if where:
            parts.append("WHERE ")
            for i, (key, value) in enumerate(where):
                if i > 0:
                    parts.append("AND ")
                parts.append(key + "='" + value + "'")
        return " ".join(parts)

    @staticmethod
    def insert(table, data):
        parts = []
        parts.append("INSERT INTO " + table + " (")
        for i, (key, value) in enumerate(data):
            parts.append(key)
            if i < len(data) - 1:
                parts.append(", ")
        parts.append(") VALUES (")
        for i, (key, value) in enumerate(data):
            parts.append("'" + value + "'")
            if i < len(data) - 1:
                parts.append(", ")
        parts.append(")")
        return "".join(parts)

    @staticmethod
    def delete_(table, where=None):
        if where is None:
            where = []
        parts = []
        parts.append("DELETE FROM " + table)
        if where:
            parts.append("WHERE ")
            for i, (key, value) in enumerate(where):
                if i > 0:
                    parts.append("AND ")
                parts.append(key + "='" + value + "'")
        return " ".join(parts)

    @staticmethod
    def update(table, data, where=None):
        if where is None:
            where = []
        parts = []
        parts.append("UPDATE " + table + " SET ")
        for i, (key, value) in enumerate(data):
            parts.append(key + "='" + value + "'")
            if i < len(data) - 1:
                parts.append(", ")
        if where:
            parts.append("WHERE ")
            for i, (key, value) in enumerate(where):
                if i > 0:
                    parts.append("AND ")
                parts.append(key + "='" + value + "'")
        return " ".join(parts)