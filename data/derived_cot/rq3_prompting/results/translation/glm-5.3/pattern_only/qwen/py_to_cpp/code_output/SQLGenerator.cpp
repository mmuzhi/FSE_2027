#include <optional>
#include <string>
#include <utility>
#include <vector>

class SQLGenerator {
public:
    explicit SQLGenerator(std::string table_name)
        : table_name_(std::move(table_name)) {}

    // fields: nullopt maps to Python None -> "*"; an empty vector maps to an
    // empty list -> empty string (same "SELECT  FROM ..." behavior as Python).
    std::string select(const std::optional<std::vector<std::string>>& fields = std::nullopt,
                       const std::optional<std::string>& condition = std::nullopt) const {
        std::string field_list;
        if (!fields.has_value()) {
            field_list = "*";
        } else {
            field_list = join(*fields, ", ");
        }
        std::string sql = "SELECT " + field_list + " FROM " + table_name_;
        if (condition.has_value()) {
            sql += " WHERE " + *condition;
        }
        return sql + ";";
    }

    // Dict keys/values are modeled as an ordered vector of pairs to preserve
    // Python dict insertion order in the generated SQL.
    std::string insert(const std::vector<std::pair<std::string, std::string>>& data) const {
        std::string fields;
        std::string values;
        bool first = true;
        for (const auto& [field, value] : data) {
            if (!first) {
                fields += ", ";
                values += ", ";
            }
            first = false;
            fields += field;
            values += "'" + value + "'";
        }
        return "INSERT INTO " + table_name_ + " (" + fields + ") VALUES (" + values + ");";
    }

    std::string update(const std::vector<std::pair<std::string, std::string>>& data,
                       const std::string& condition) const {
        std::string set_clause = join_assignments(data, ", ");
        return "UPDATE " + table_name_ + " SET " + set_clause + " WHERE " + condition + ";";
    }

    // "delete" is a reserved keyword in C++; delete_ keeps the closest name.
    std::string delete_(const std::string& condition) const {
        return "DELETE FROM " + table_name_ + " WHERE " + condition + ";";
    }

    std::string select_female_under_age(int age) const {
        std::string condition = "age < " + std::to_string(age) + " AND gender = 'female'";
        return select(std::nullopt, condition);
    }

    std::string select_by_age_range(int min_age, int max_age) const {
        std::string condition =
            "age BETWEEN " + std::to_string(min_age) + " AND " + std::to_string(max_age);
        return select(std::nullopt, condition);
    }

private:
    std::string table_name_;

    static std::string join(const std::vector<std::string>& items, const std::string& sep) {
        std::string result;
        bool first = true;
        for (const auto& item : items) {
            if (!first) result += sep;
            first = false;
            result += item;
        }
        return result;
    }

    static std::string join_assignments(
        const std::vector<std::pair<std::string, std::string>>& items,
        const std::string& sep) {
        std::string result;
        bool first = true;
        for (const auto& [field, value] : items) {
            if (!first) result += sep;
            first = false;
            result += field + " = '" + value + "'";
        }
        return result;
    }
};