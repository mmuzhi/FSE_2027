#include <string>
#include <vector>
#include <algorithm>

class SQLGenerator {
private:
    std::string table_name;

public:
    explicit SQLGenerator(const std::string& table_name) : table_name(table_name) {}

    std::string select(const std::vector<std::string>& fields = {}, const std::string& condition = "") {
        std::string sql;
        if (fields.empty()) {
            sql = "*";
        } else {
            sql = "";
            for (size_t i = 0; i < fields.size(); ++i) {
                if (i != 0) sql += ", ";
                sql += fields[i];
            }
        }
        sql += " FROM " + table_name;
        if (!condition.empty()) {
            sql += " WHERE " + condition;
        }
        return sql + ';';
    }

    std::string insert(const std::vector<std::pair<std::string, std::string>>& data) {
        if (data.empty()) {
            return "INSERT INTO " + table_name + "() VALUES ();";
        }
        std::string fields, values;
        for (size_t i = 0; i < data.size(); ++i) {
            if (i != 0) fields += ", ";
            fields += data[i].first;
            if (i != 0) values += ", ";
            values += '\'' + data[i].second + '\'';
        }
        return "INSERT INTO " + table_name + " (" + fields + ") VALUES (" + values + ");";
    }

    std::string update(const std::vector<std::pair<std::string, std::string>>& data, const std::string& condition) {
        if (data.empty()) {
            return "UPDATE " + table_name + " SET  WHERE " + condition + ';';
        }
        std::string set_clause;
        for (size_t i = 0; i < data.size(); ++i) {
            if (i != 0) set_clause += ", ";
            set_clause += data[i].first + " = '" + data[i].second + "'";
        }
        return "UPDATE " + table_name + " SET " + set_clause + " WHERE " + condition + ';';
    }

    std::string delete_(const std::string& condition) {
        return "DELETE FROM " + table_name + " WHERE " + condition + ';';
    }

    std::string select_female_under_age(int age) {
        return select({}, "age < " + std::to_string(age) + " AND gender = 'female'");
    }

    std::string select_by_age_range(int min_age, int max_age) {
        return select({}, "age BETWEEN " + std::to_string(min_age) + " AND " + std::to_string(max_age));
    }
};