import re


class SQLQueryBuilder:
    @staticmethod
    def _java_str(s):
        return "null" if s is None else str(s)

    @staticmethod
    def _split_columns(columns):
        # Mimics Java String.split(",\\s*"), including removal of trailing empty strings.
        if columns == "":
            return [""]
        parts = re.split(r",\s*", columns)
        while parts and parts[-1] == "":
            parts.pop()
        return parts

    @staticmethod
    def select(table, columns, where=None):
        if columns is None:
            columns = "*"

        if isinstance(columns, str):
            columns = SQLQueryBuilder._split_columns(columns)
        else:
            columns = list(columns)

        query = "SELECT "
        if len(columns) > 0:
            query += ", ".join(SQLQueryBuilder._java_str(c) for c in columns)
        else:
            query += "*"

        query += " FROM " + SQLQueryBuilder._java_str(table)

        if where is not None and where:
            query += " WHERE "
            first = True
            for key, value in where.items():
                if not first:
                    query += " AND "
                query += SQLQueryBuilder._java_str(key) + "='" + SQLQueryBuilder._java_str(value) + "'"
                first = False

        return query

    @staticmethod
    def insert(table, data):
        query = "INSERT INTO " + SQLQueryBuilder._java_str(table) + " ("
        values = " VALUES ("

        first = True
        for key, value in data.items():
            if not first:
                query += ", "
                values += ", "
            query += SQLQueryBuilder._java_str(key)
            values += "'" + SQLQueryBuilder._java_str(value) + "'"
            first = False

        query += ")"
        values += ")"
        return query + values

    @staticmethod
    def delete(table, where=None):
        query = "DELETE FROM " + SQLQueryBuilder._java_str(table)

        if where is not None and where:
            query += " WHERE "
            first = True
            for key, value in where.items():
                if not first:
                    query += " AND "
                query += SQLQueryBuilder._java_str(key) + "='" + SQLQueryBuilder._java_str(value) + "'"
                first = False

        return query

    @staticmethod
    def update(table, data, where=None):
        query = "UPDATE " + SQLQueryBuilder._java_str(table) + " SET "

        first = True
        for key, value in data.items():
            if not first:
                query += ", "
            query += SQLQueryBuilder._java_str(key) + "='" + SQLQueryBuilder._java_str(value) + "'"
            first = False

        if where is not None and where:
            query += " WHERE "
            first = True
            for key, value in where.items():
                if not first:
                    query += " AND "
                query += SQLQueryBuilder._java_str(key) + "='" + SQLQueryBuilder._java_str(value) + "'"
                first = False

        return query