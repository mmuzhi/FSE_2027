#include <string>
#include <vector>
#include <optional>
#include <utility>

class SQLGenerator {
private:
    std::string table_name;

    static std::string join(const std::vector<std::string>& parts, const std::string& delimiter) {
        std::string result;
        for (size_t i = 0; i < parts.size(); ++i) {
            if (i > 0) result += delimiter;
            result += parts[i];
        }
        return result;
    }

public:
    SQLGenerator(const std::string& table_name) : table_name(table_name) {}

    std::string select(const std::optional<std::vector<std::string>>& fields = std::nullopt,
                       const std::optional<std::string>& condition = std::nullopt) {
        std::string fields_str = fields.has_value() ? join(*fields, ", ") : "*";
        std::string sql = "SELECT " + fields_str + " FROM " + table_name;
        if (condition.has_value()) {
            sql += " WHERE " + *condition;
        }
        return sql + ";";
    }

    // Uses vector<pair> to preserve insertion order (matching Python dict ordering)
    std::string insert(const std::vector<std::pair<std::string, std::string>>& data) {
        std::vector<std::string> fields_list;
        std::vector<std::string> values_list;
        for (const auto& [field, value] : data) {
            fields_list.push_back(field);
            values_list.push_back("'" + value + "'");
        }
        return "INSERT INTO " + table_name + " (" + join(fields_list, ", ") +
               ") VALUES (" + join(values_list, ", ") + ");";
    }

    std::string update(const std::vector<std::pair<std::string, std::string>>& data,
                       const std::string& condition) {
        std::vector<std::string> set_parts;
        for (const auto& [field, value] : data) {
            set_parts.push_back(field + " = '" + value + "'");
        }
        return "UPDATE " + table_name + " SET " + join(set_parts, ", ") +
               " WHERE " + condition + ";";
    }

    // Named delete_from since 'delete' is a C++ keyword
    std::string delete_from(const std::string& condition) {
        return "DELETE FROM " + table_name + " WHERE " + condition + ";";
    }

    std::string select_female_under_age(int age) {
        std::string condition = "age < " + std::to_string(age) + " AND gender = 'female'";
        return select(std::nullopt, condition);
    }

    std::string select_by_age_range(int min_age, int max_age) {
        std::string condition = "age BETWEEN " + std::to_string(min_age) +
                                " AND " + std::to_string(max_age);
        return select(std::nullopt, condition);
    }
};