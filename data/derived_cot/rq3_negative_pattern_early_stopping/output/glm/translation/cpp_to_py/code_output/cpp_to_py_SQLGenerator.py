class SQLGenerator:
    def __init__(self, table_name):
        self.table_name = table_name

    def select(self, fields=None, condition=""):
        if fields is None:
            fields = []
        
        if not fields:
            fields_str = "*"
        else:
            fields_str = ", ".join(fields)
        
        sql = f"SELECT {fields_str} FROM {self.table_name}"
        if condition:
            sql += f" WHERE {condition}"
        return sql + ";"

    def insert(self, data):
        fields = []
        values = []
        for k, v in sorted(data.items()):
            fields.append(k)
            values.append(f"'{v}'")
            
        fields_str = ", ".join(fields)
        values_str = ", ".join(values)
        sql = f"INSERT INTO {self.table_name} ({fields_str}) VALUES ({values_str})"
        return sql + ";"

    def update(self, data, condition):
        set_parts = []
        for k, v in sorted(data.items()):
            set_parts.append(f"{k} = '{v}'")
            
        set_clause = ", ".join(set_parts)
        sql = f"UPDATE {self.table_name} SET {set_clause}"
        if condition:
            sql += f" WHERE {condition}"
        return sql + ";"

    def delete_query(self, condition):
        sql = f"DELETE FROM {self.table_name}"
        if condition:
            sql += f" WHERE {condition}"
        return sql + ";"

    def select_female_under_age(self, age):
        condition = f"age < {age} AND gender = 'female'"
        return self.select([], condition)

    def select_by_age_range(self, min_age, max_age):
        condition = f"age BETWEEN {min_age} AND {max_age}"
        return self.select([], condition)