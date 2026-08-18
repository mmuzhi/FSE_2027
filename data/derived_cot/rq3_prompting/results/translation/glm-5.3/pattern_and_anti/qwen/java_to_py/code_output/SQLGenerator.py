class SQLGenerator:
    def __init__(self, table_name):
        self.table_name = table_name

    def select(self, fields, condition):
        fields_str = "*" if fields is None else ", ".join(fields)
        sql = "SELECT " + fields_str + " FROM " + self.table_name
        if condition is not None:
            sql += " WHERE " + condition
        return sql + ";"

    def insert(self, data):
        sorted_data = dict(sorted(data.items()))
        fields = ", ".join(sorted_data.keys())
        values = ", ".join("'" + value + "'" for value in sorted_data.values())
        return "INSERT INTO " + self.table_name + " (" + fields + ") VALUES (" + values + ");"

    def update(self, data, condition):
        sorted_data = dict(sorted(data.items()))
        set_clause = ", ".join(key + " = '" + value + "'" for key, value in sorted_data.items())
        return "UPDATE " + self.table_name + " SET " + set_clause + " WHERE " + condition + ";"

    def delete(self, condition):
        return "DELETE FROM " + self.table_name + " WHERE " + condition + ";"

    def select_female_under_age(self, age):
        return "SELECT * FROM " + self.table_name + " WHERE age < " + str(age) + " AND gender = 'female';"

    def select_by_age_range(self, min_age, max_age):
        return "SELECT * FROM " + self.table_name + " WHERE age BETWEEN " + str(min_age) + " AND " + str(max_age) + ";"