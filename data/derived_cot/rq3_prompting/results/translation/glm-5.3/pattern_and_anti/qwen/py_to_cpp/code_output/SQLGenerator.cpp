#include <string>
#include <vector>
#include <utility>
#include <optional>
#include <sstream>

// Note: `delete` is a C++ keyword, so the method is named `delete_`.
// Data is represented as a vector of (key, value) pairs to preserve
// Python dict insertion order (which affects the generated SQL text).

class SQLGenerator {
public:
    using DataRow = std::vector<std::pair<std::string, std::string>>;

    explicit SQLGenerator(std::string table_name)
        : table_name_(std::move(table_name)) {}

    std::string select(const std::optional<std::vector<std::string>>& fields = std::nullopt,
                       const std::optional<std::string>& condition = std::nullopt) const {
        std::string fieldList = "*";
        if (fields.has_value()) {
            std::ostringstream ss;
            for (size_t i = 0; i < fields->size(); ++i) {
                if (i > 0) ss << ", ";
                ss << (*fields)[i];
            }
            fieldList = ss.str();
        }
        std::string sql = "SELECT " + fieldList + " FROM " + table_name_;
        if (condition.has_value()) {
            sql += " WHERE " + *condition;
        }
        return sql + ";";
    }

    std::string insert(const DataRow& data) const {
        std::ostringstream fields, values;
        for (size_t i = 0; i < data.size(); ++i) {
            if (i > 0) {
                fields << ", ";
                values << ", ";
            }
            fields << data[i].first;
            values << "'" << data[i].second << "'";
        }
        return "INSERT INTO " + table_name_ + " (" + fields.str() + ") VALUES (" + values.str() + ");";
    }

    std::string update(const DataRow& data, const std::string& condition) const {
        std::ostringstream setClause;
        for (size_t i = 0; i < data.size(); ++i) {
            if (i > 0) setClause << ", ";
            setClause << data[i].first << " = '" << data[i].second << "'";
        }
        return "UPDATE " + table_name_ + " SET " + setClause.str() + " WHERE " + condition + ";";
    }

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
};