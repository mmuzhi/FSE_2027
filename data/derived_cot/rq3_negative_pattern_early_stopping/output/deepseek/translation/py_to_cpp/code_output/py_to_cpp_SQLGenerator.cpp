#include <string>
#include <vector>
#include <map>
#include <sstream>

class SQLGenerator {
private:
    std::string table_name;

    static std::string join(const std::vector<std::string>& vec, const std::string& delimiter) {
        if (vec.empty()) return "";
        std::ostringstream oss;
        auto it = vec.begin();
        oss << *it;
        ++it;
        while (it != vec.end()) {
            oss << delimiter << *it;
            ++it;
        }
        return oss.str();
    }

public:
    explicit SQLGenerator(const std::string& table_name) : table_name(table_name) {}

    std::string select(const std::vector<std::string>* fields = nullptr, const std::string* condition = nullptr) {
        std::string fields_str;
        if (fields == nullptr) {
            fields_str = "*";
        } else {
            fields_str = join(*fields, ", ");
        }
        std::string sql = "SELECT " + fields_str + " FROM " + table_name;
        if (condition != nullptr) {
            sql += " WHERE " + *condition;
        }
        return sql + ";";
    }

    std::string insert(const std::map<std::string, std::string>& data) {
        std::vector<std::string> field_names;
        std::vector<std::string> value_strs;
        for (const auto& [key, value] : data) {
            field_names.push_back(key);
            value_strs.push_back("'" + value + "'");
        }
        std::string fields = join(field_names, ", ");
        std::string values = join(value_strs, ", ");
        return "INSERT INTO " + table_name + " (" + fields + ") VALUES (" + values + ");";
    }

    std::string update(const std::map<std::string, std::string>& data, const std::string& condition) {
        std::vector<std::string> set_parts;
        for (const auto& [key, value] : data) {
            set_parts.push_back(key + " = '" + value + "'");
        }
        std::string set_clause = join(set_parts, ", ");
        return "UPDATE " + table_name + " SET " + set_clause + " WHERE " + condition + ";";
    }

    std::string del(const std::string& condition) {
        return "DELETE FROM " + table_name + " WHERE " + condition + ";";
    }

    std::string select_female_under_age(int age) {
        std::string condition = "age < " + std::to_string(age) + " AND gender = 'female'";
        return select(nullptr, &condition);
    }

    std::string select_by_age_range(int min_age, int max_age) {
        std::string condition = "age BETWEEN " + std::to_string(min_age) + " AND " + std::to_string(max_age);
        return select(nullptr, &condition);
    }
};