class SQLGenerator:
    def __init__(self, table_name):
        self.table_name = table_name

    def select(self, fields=None, condition=None):
        fields_str = '*' if fields is None else ', '.join(fields)
        sql = f'SELECT {fields_str} FROM {self.table_name}'
        if condition is not None:
            sql += f' WHERE {condition}'
        return sql + ';'

    def insert(self, data):
        sorted_data = sorted(data.items())
        fields = ', '.join(item[0] for item in sorted_data)
        values = ', '.join(f"'{value}'" for key, value in sorted_data)
        return f'INSERT INTO {self.table_name} ({fields}) VALUES ({values});'

    def update(self, data, condition):
        sorted_data = sorted(data.items())
        set_clause = ', '.join(f'{key} = "{value}"' for key, value in sorted_data)
        return f'UPDATE {self.table_name} SET {set_clause} WHERE {condition};'

    def delete(self, condition):
        return f'DELETE FROM {self.table_name} WHERE {condition};'

    def select_female_under_age(self, age):
        return f'SELECT * FROM {self.table_name} WHERE age < {age} AND gender = "female";'

    def select_by_age_range(self, min_age, max_age):
        return f'SELECT * FROM {self.table_name} WHERE age BETWEEN {min_age} AND {max_age};'