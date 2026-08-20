from typing import Dict, List, Optional


class SQLGenerator:
    def __init__(self, table_name: str) -> None:
        self.table_name = table_name

    def select(self, fields: Optional[List[str]], condition: Optional[str]) -> str:
        fields_str = "*" if fields is None else ", ".join(fields)
        sql = f"SELECT {fields_str} FROM {self.table_name}"
        if condition is not None:
            sql += f" WHERE {condition}"
        return sql + ";"

    def insert(self, data: Dict[str, str]) -> str:
        sorted_items = sorted(data.items())
        fields = ", ".join(key for key, _ in sorted_items)
        values = ", ".join(f"'{value}'" for _, value in sorted_items)
        return f"INSERT INTO {self.table_name} ({fields}) VALUES ({values});"

    def update(self, data: Dict[str, str], condition: str) -> str:
        set_clause = ", ".join(f"{key} = '{value}'" for key, value in sorted(data.items()))
        return f"UPDATE {self.table_name} SET {set_clause} WHERE {condition};"

    def delete(self, condition: str) -> str:
        return f"DELETE FROM {self.table_name} WHERE {condition};"

    def selectFemaleUnderAge(self, age: int) -> str:
        return f"SELECT * FROM {self.table_name} WHERE age < {age} AND gender = 'female';"

    def selectByAgeRange(self, min_age: int, max_age: int) -> str:
        return f"SELECT * FROM {self.table_name} WHERE age BETWEEN {min_age} AND {max_age};"