#include <optional>
#include <string>
#include <vector>
#include <sstream>
#include <utility>

class SQLGenerator {
public:
    std::string table_name;

    explicit SQLGenerator(std::string table_name) : table_name(std::move(table_name)) {}

    std::string select(std::optional<std::vector<std::string>> fields = std::nullopt,
                       std::optional<std::string> condition = std::nullopt) const {
        std::string fields_str = "*";
        if (fields.has_value()) {
            fields_str = join(*fields, ", ");
        }
        std::string sql = "SELECT " + fields_str + " FROM " + table_name;
        if (condition.has_value()) {
            sql += " WHERE " + *condition;
        }
        return sql + ";";
    }

    std::string insert(const std::vector<std::pair<std::string, std::string>>& data) const {
        std::vector<std::string> fields;
        std::vector<std::string> values;
        for (const auto& item : data) {
            fields.push_back(item.first);
            values.push_back("'" + item.second + "'");
        }
        std::string sql = "INSERT INTO " + table_name + " (" + join(fields, ", ") + ") VALUES (" + join(values, ", ") + ")";
        return sql + ";";
    }

    std::string update(const std::vector<std::pair<std::string, std::string>>& data, const std::string& condition) const {
        std::vector<std::string> set_clause;
        for (const auto& item : data) {
            set_clause.push_back(item.first + " = '" + item.second + "'");
        }
        std::string sql = "UPDATE " + table_name + " SET " + join(set_clause, ", ") + " WHERE " + condition;
        return sql + ";";
    }

    // `delete` is a C++ keyword, so this method is named `delete_`.
    std::string delete_(const std::string& condition) const {
        std::string sql = "DELETE FROM " + table_name + " WHERE " + condition;
        return sql + ";";
    }

    std::string select_female_under_age(int age) const {
        std::string condition = "age < " + std::to_string(age) + " AND gender = 'female'";
        return select(std::nullopt, condition);
    }

    std::string select_by_age_range(int min_age, int max_age) const {
        std::string condition = "age BETWEEN " + std::to_string(min_age) + " AND " + std::to_string(max_age);
        return select(std::nullopt, condition);
    }

private:
    static std::string join(const std::vector<std::string>& vec, const std::string& delimiter) {
        std::ostringstream oss;
        for (size_t i = 0; i < vec.size(); ++i) {
            if (i != 0) oss << delimiter;
            oss << vec[i];
        }
        return oss.str();
    }
};