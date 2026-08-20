import re

# Java's String.split(",\\s*") uses Java's default (ASCII) whitespace class
# for \s, hence the re.ASCII flag here.
_COMMA_WS = re.compile(r",\s*", re.ASCII)


def _jstr(value):
    # Java's StringBuilder.append / String.valueOf / String.join render null
    # as the string "null".
    return "null" if value is None else str(value)


def _java_split(columns):
    # Equivalent of Java's String.split(",\\s*"): Java discards trailing
    # empty strings, but when the pattern never matches, the input is
    # returned as a single-element array.
    parts = _COMMA_WS.split(columns)
    if len(parts) > 1:  # the pattern matched at least once
        while parts and parts[-1] == "":
            parts.pop()
    return parts


def _where_clause(where):
    # Mirrors `where != null && !where.isEmpty()`; entries keep insertion
    # order just like a LinkedHashMap (Python dicts are ordered).
    if where:
        conditions = [
            _jstr(key) + "='" + _jstr(value) + "'" for key, value in where.items()
        ]
        return " WHERE " + " AND ".join(conditions)
    return ""


class SQLQueryBuilder:

    @staticmethod
    def select(table, columns, where):
        # The Java code has two overloads: (String columns) and (String[]
        # columns). Strings (and None, which becomes "*") go through the
        # split path; other sequences are used directly, like the array
        # overload.
        if columns is None:
            columns = "*"
        if isinstance(columns, str):
            columns = _java_split(columns)

        if len(columns) > 0:
            column_sql = ", ".join(_jstr(column) for column in columns)
        else:
            column_sql = "*"

        return "SELECT " + column_sql + " FROM " + _jstr(table) + _where_clause(where)

    @staticmethod
    def insert(table, data):
        keys = []
        values = []
        for key, value in data.items():
            keys.append(_jstr(key))
            values.append("'" + _jstr(value) + "'")

        return (
            "INSERT INTO " + _jstr(table) + " ("
            + ", ".join(keys)
            + ") VALUES ("
            + ", ".join(values)
            + ")"
        )

    @staticmethod
    def delete(table, where):
        return "DELETE FROM " + _jstr(table) + _where_clause(where)

    @staticmethod
    def update(table, data, where):
        assignments = ", ".join(
            _jstr(key) + "='" + _jstr(value) + "'" for key, value in data.items()
        )
        return "UPDATE " + _jstr(table) + " SET " + assignments + _where_clause(where)