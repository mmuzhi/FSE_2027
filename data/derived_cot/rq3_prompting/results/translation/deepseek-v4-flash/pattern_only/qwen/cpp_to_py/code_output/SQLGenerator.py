class SQLGenerator:
    def __init__(self, table_name):
        self.table_name = table_name

    def select(self, fields=None, condition=""):
        if fields is None:
            fields = []
        if fields:
            fields_str = ", ".join(fields)
        else:
            fields_str = "*"

        sql = "SELECT " + fields_str + " FROM " + self.table_name
        if condition:
            sql += " WHERE " + condition
        return sql + ";"

    def insert(self, data):
        fields = []
        values = []
        for key in sorted(data):
            fields.append(key)
            values.append("'" + data[key] + "'")

        sql = "INSERT INTO " + self.table_name + " (" + ", ".join(fields) + ") VALUES (" + ", ".join(values) + ")"
        return sql + ";"

    def update(self, data, condition):
        set_clause = []
        for key in sorted(data):
            set_clause.append(key + " = '" + data[key] + "'")

        sql = "UPDATE " + self.table_name + " SET " + ", ".join(set_clause)
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