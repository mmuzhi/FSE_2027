class SQLGenerator:
    def __init__(self, table_name):
        self.table_name = table_name

    def select(self, fields=(), condition=""):
        if fields:
            fields_str = ", ".join(fields)
        else:
            fields_str = "*"

        sql = "SELECT " + fields_str + " FROM " + self.table_name
        if condition:
            sql += " WHERE " + condition
        return sql + ";"

    def insert(self, data):
        # sorted() mirrors std::map's ordered (key-sorted) iteration
        fields_stream = []
        values_stream = []
        for key in sorted(data):
            fields_stream.append(key)
            values_stream.append("'" + data[key] + "'")

        sql = ("INSERT INTO " + self.table_name + " ("
               + ", ".join(fields_stream) + ") VALUES ("
               + ", ".join(values_stream) + ")")
        return sql + ";"

    def update(self, data, condition):
        # sorted() mirrors std::map's ordered (key-sorted) iteration
        set_clause_stream = []
        for key in sorted(data):
            set_clause_stream.append(key + " = '" + data[key] + "'")

        sql = "UPDATE " + self.table_name + " SET " + ", ".join(set_clause_stream)
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