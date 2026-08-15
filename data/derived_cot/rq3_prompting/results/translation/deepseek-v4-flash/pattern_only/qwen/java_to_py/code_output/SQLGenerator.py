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
        sorted_keys = sorted(data.keys())
        fields = ", ".join(sorted_keys)
        values = ", ".join("'" + data[k] + "'" for k in sorted_keys)
        return "INSERT INTO " + self.table_name + " (" + fields + ") VALUES (" + values + ");"

    def update(self, data, condition):
        sorted_keys = sorted(data.keys())
        set_clause = ", ".join(k + " = '" + data[k] + "'" for k in sorted_keys)
        return "UPDATE " + self.table_name + " SET " + set_clause + " WHERE " + condition + ";"

    def delete(self, condition):
        return "DELETE FROM " + self.table_name + " WHERE " + condition + ";"

    def selectFemaleUnderAge(self, age):
        return "SELECT * FROM " + self.table_name + " WHERE age < " + str(age) + " AND gender = 'female';"

    def selectByAgeRange(self, minAge, maxAge):
        return "SELECT * FROM " + self.table_name + " WHERE age BETWEEN " + str(minAge) + " AND " + str(maxAge) + ";"