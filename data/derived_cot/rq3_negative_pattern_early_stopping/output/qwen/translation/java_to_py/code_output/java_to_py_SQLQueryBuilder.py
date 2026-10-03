class SQLQueryBuilder:

    @staticmethod
    def select(table, columns=None, where=None):
        if columns is None:
            columns = "*"
        else:
            # If columns is a string, split it into a list
            if isinstance(columns, str):
                columns = [col.strip() for col in columns.split(",")]
            # If it's already a list, we keep it

        # Now columns is either a list or the string "*"
        if columns == "*":
            col_str = "*"
        else:
            col_str = ", ".join(columns)

        query = f"SELECT {col_str} FROM {table}"

        if where is not None and len(where) > 0:
            query += " WHERE "
            first = True
            for key, value in where.items():
                if not first:
                    query += " AND "
                else:
                    first = False
                # We are using single quotes around the value
                query += f"{key}='{value}'"
        return query

    @staticmethod
    def insert(table, data):
        if not data:
            raise ValueError("Data map must not be empty for insert")
        query = f"INSERT INTO {table} ("
        values = " VALUES ("
        first = True
        for key, value in data.items():
            if not first:
                query += ", "
                values += ", "
            else:
                first = False
            query += f"{key}"
            values += f"'{value}'"
        query += ")"
        values += ")"
        return query + values

    @staticmethod
    def delete(table, where=None):
        query = f"DELETE FROM {table}"
        if where is not None and len(where) > 0:
            query += " WHERE "
            first = True
            for key, value in where.items():
                if not first:
                    query += " AND "
                else:
                    first = False
                query += f"{key}='{value}'"
        return query

    @staticmethod
    def update(table, data, where=None):
        query = f"UPDATE {table} SET "
        if not data:
            raise ValueError("Data map must not be empty for update")
        first = True
        for key, value in data.items():
            if not first:
                query += ", "
            else:
                first = False
            query += f"{key}='{value}'"
        if where is not None and len(where) > 0:
            query += " WHERE "
            first = True
            for key, value in where.items():
                if not first:
                    query += " AND "
                else:
                    first = False
                query += f"{key}='{value}'"
        return query