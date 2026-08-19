class SQLGenerator:
    def __init__(self, table_name):
        self.table_name = table_name

    def select(self, fields=None, condition=""):
        if fields is None:
            fields = []
        if fields:
            fields_str = fields[0]
            for field in fields[1:]:
                fields_str += ", " + field
        else:
            fields_str = "*"

        sql = "SELECT " + fields_str + " FROM " + self.table_name
        if condition:
            sql += " WHERE " + condition
        return sql + ";"

    def insert(self, data):
        fields_list = []
        values_list = []
        # std::map iterates in sorted key order; mirror that for identical output
        for key in sorted(data.keys()):
            fields_list.append(key)
            values_list.append("'" + data[key] + "'")

        sql = ("INSERT INTO " + self.table_name + " ("
               + ", ".join(fields_list) + ") VALUES ("
               + ", ".join(values_list) + ")")
        return sql + ";"

    def update(self, data, condition):
        set_parts = []
        # std::map iterates in sorted key order; mirror that for identical output
        for key in sorted(data.keys()):
            set_parts.append(key + " = '" + data[key] + "'")

        sql = "UPDATE " + self.table_name + " SET " + ", ".join(set_parts)
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