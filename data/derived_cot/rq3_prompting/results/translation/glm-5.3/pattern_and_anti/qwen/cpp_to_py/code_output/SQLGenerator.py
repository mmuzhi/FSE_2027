from typing import Dict, List, Optional, Sequence


class SQLGenerator:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def select(self, fields: Optional[Sequence[str]] = None, condition: str = "") -> str:
        fields = fields if fields is not None else []
        if fields:
            fields_str = fields[0]
            for i in range(1, len(fields)):
                fields_str += ", " + fields[i]
        else:
            fields_str = "*"

        sql = "SELECT " + fields_str + " FROM " + self.table_name
        if condition:
            sql += " WHERE " + condition
        return sql + ";"

    def insert(self, data: Dict[str, str]) -> str:
        fields_list = []
        values_list = []
        for key, value in sorted(data.items()):
            fields_list.append(key)
            values_list.append("'" + value + "'")

        sql = ("INSERT INTO " + self.table_name + " ("
               + ", ".join(fields_list) + ") VALUES ("
               + ", ".join(values_list) + ")")
        return sql + ";"

    def update(self, data: Dict[str, str], condition: str) -> str:
        set_clause = ", ".join(
            key + " = '" + value + "'" for key, value in sorted(data.items())
        )

        sql = "UPDATE " + self.table_name + " SET " + set_clause
        if condition:
            sql += " WHERE " + condition
        return sql + ";"

    def delete_query(self, condition: str) -> str:
        sql = "DELETE FROM " + self.table_name
        if condition:
            sql += " WHERE " + condition
        return sql + ";"

    def select_female_under_age(self, age: int) -> str:
        condition = "age < " + str(age) + " AND gender = 'female'"
        return self.select([], condition)

    def select_by_age_range(self, min_age: int, max_age: int) -> str:
        condition = "age BETWEEN " + str(min_age) + " AND " + str(max_age)
        return self.select([], condition)