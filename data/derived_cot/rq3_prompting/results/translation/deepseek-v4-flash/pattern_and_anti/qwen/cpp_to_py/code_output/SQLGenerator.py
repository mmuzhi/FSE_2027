class SQLGenerator:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def select(self, fields=None, condition: str = "") -> str:
        if fields is None:
            fields = []

        if fields:
            fields_str = ", ".join(fields)
        else:
            fields_str = "*"

        sql = f"SELECT {fields_str} FROM {self.table_name}"
        if condition:
            sql += f" WHERE {condition}"
        return sql + ";"

    def insert(self, data: dict) -> str:
        fields_list = []
        values_list = []
        for key, value in sorted(data.items()):
            fields_list.append(key)
            values_list.append(f"'{value}'")

        fields_str = ", ".join(fields_list)
        values_str = ", ".join(values_list)

        sql = f"INSERT INTO {self.table_name} ({fields_str}) VALUES ({values_str})"
        return sql + ";"

    def update(self, data: dict, condition: str = "") -> str:
        set_clause = ", ".join(f"{key} = '{value}'" for key, value in sorted(data.items()))

        sql = f"UPDATE {self.table_name} SET {set_clause}"
        if condition:
            sql += f" WHERE {condition}"
        return sql + ";"

    def delete_query(self, condition: str = "") -> str:
        sql = f"DELETE FROM {self.table_name}"
        if condition:
            sql += f" WHERE {condition}"
        return sql + ";"

    def select_female_under_age(self, age: int) -> str:
        condition = f"age < {age} AND gender = 'female'"
        return self.select(condition=condition)

    def select_by_age_range(self, min_age: int, max_age: int) -> str:
        condition = f"age BETWEEN {min_age} AND {max_age}"
        return self.select(condition=condition)