import re


def _jstr(value):
    # Java's StringBuilder.append(String)/String.valueOf: None renders as "null"
    return "null" if value is None else str(value)


def _java_split(s, pattern=r",\s*"):
    # Java's String.split: trailing empty strings are discarded;
    # an empty input yields a single empty string.
    if s == "":
        return [""]
    parts = re.split(pattern, s, flags=re.ASCII)
    while parts and parts[-1] == "":
        parts.pop()
    return parts


def _append_where(query, where):
    # Mirrors the shared WHERE-building block (dict preserves insertion
    # order, matching LinkedHashMap iteration order).
    if where is not None and len(where) > 0:
        query += " WHERE "
        first = True
        for key, value in where.items():
            if not first:
                query += " AND "
            query += f"{_jstr(key)}='{_jstr(value)}'"
            first = False
    return query


def select(table, columns, where):
    # Unifies the two Java overloads: columns may be None, a comma
    # separated string, or a list of column names.
    if columns is None:
        columns = "*"
    if isinstance(columns, str):
        columns = _java_split(columns)
    query = "SELECT "
    if len(columns) > 0:
        query += ", ".join(_jstr(c) for c in columns)
    else:
        query += "*"
    query += f" FROM {_jstr(table)}"
    return _append_where(query, where)


def insert(table, data):
    query = f"INSERT INTO {_jstr(table)} ("
    values = " VALUES ("

    first = True
    for key, value in data.items():
        if not first:
            query += ", "
            values += ", "
        query += _jstr(key)
        values += f"'{_jstr(value)}'"
        first = False

    query += ")"
    values += ")"

    return query + values


def delete(table, where):
    return _append_where(f"DELETE FROM {_jstr(table)}", where)


def update(table, data, where):
    query = f"UPDATE {_jstr(table)} SET "

    first = True
    for key, value in data.items():
        if not first:
            query += ", "
        query += f"{_jstr(key)}='{_jstr(value)}'"
        first = False

    return _append_where(query, where)