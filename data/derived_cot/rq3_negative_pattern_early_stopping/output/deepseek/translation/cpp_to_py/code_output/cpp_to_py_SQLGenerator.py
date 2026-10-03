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
        sql = "SELECT " + fields_str + " FROM " + self.table_name
        if condition:
            sql += " WHERE " + condition
        return sql + ";"

    def insert(self, data):
        keys = sorted(data.keys())
        fields_str = ", ".join(keys)
        values_str = ", ".join("'" + data[k] + "'" for k in keys)
        sql = "INSERT INTO " + self.table_name + " (" + fields_str + ") VALUES (" + values_str + ")"
        return sql + ";"

    def update(self, data, condition):
        keys = sorted(data.keys())
        set_clause = ", ".join(k + " = '" + data[k] + "'" for k in keys)
        sql = "UPDATE " + self.table_name + " SET " + set_clause
        if condition:
            sql += " WHERE " + condition
        return sql + ";"

    def delete_query(self, condition):
        sql = "DELETE FROM " + self.table_name
        if condition:
            sql += " WHERE " + condition
        return sql + ";"

    def select_female_under_age(self, age):
        condition = "age < " + str(age) + " AND gender = 'female'"
        return self.select([], condition)

    def select_by_age_range(self, min_age, max_age):
        condition = "age BETWEEN " + str(min_age) + " AND " + str(max_age)
        return self.select([], condition)