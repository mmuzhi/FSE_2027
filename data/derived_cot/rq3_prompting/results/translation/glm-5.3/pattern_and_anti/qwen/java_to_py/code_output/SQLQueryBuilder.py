import re


def _jstr(value):
    # Java StringBuilder.append((String) null) appends the literal "null"
    return "null" if value is None else str(value)


def _split_columns(columns):
    # Mimics Java's columns.split(",\\s*") exactly:
    # trailing empty strings are dropped, but a no-match input keeps one element.
    parts = re.split(r",\s*", columns)
    while len(parts) > 1 and parts[-1] == "":
        parts.pop()
    return parts


class SQLQueryBuilder:

    @staticmethod
    def select(table, columns, where):
        # Covers both Java overloads: String columns (comma-separated) and array of columns.
        if columns is None:
            columns = "*"
        if isinstance(columns, str):
            columns = _split_columns(columns)

        query = "SELECT "
        if len(columns) > 0:
            query += ", ".join(_jstr(c) for c in columns)
        else:
            query += "*"
        query += " FROM " + _jstr(table)

        if where is not None and len(where) > 0:
            query += " WHERE "
            first = True
            for key, value in where.items():
                if not first:
                    query += " AND "
                query += _jstr(key) + "='" + _jstr(value) + "'"
                first = False
        return query

    @staticmethod
    def insert(table, data):
        query = "INSERT INTO " + _jstr(table) + " ("
        values = " VALUES ("

        first = True
        for key, value in data.items():
            if not first:
                query += ", "
                values += ", "
            query += _jstr(key)
            values += "'" + _jstr(value) + "'"
            first = False

        query += ")"
        values += ")"

        return query + values

    @staticmethod
    def delete(table, where):
        query = "DELETE FROM " + _jstr(table)

        if where is not None and len(where) > 0:
            query += " WHERE "
            first = True
            for key, value in where.items():
                if not first:
                    query += " AND "
                query += _jstr(key) + "='" + _jstr(value) + "'"
                first = False
        return query

    @staticmethod
    def update(table, data, where):
        query = "UPDATE " + _jstr(table) + " SET "

        first = True
        for key, value in data.items():
            if not first:
                query += ", "
            query += _jstr(key) + "='" + _jstr(value) + "'"
            first = False

        if where is not None and len(where) > 0:
            query += " WHERE "
            first_where = True
            for key, value in where.items():
                if not first_where:
                    query += " AND "
                query += _jstr(key) + "='" + _jstr(value) + "'"
                first_where = False
        return query