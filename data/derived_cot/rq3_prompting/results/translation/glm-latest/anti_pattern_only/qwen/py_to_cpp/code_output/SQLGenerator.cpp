#include <cstddef>
#include <optional>
#include <string>
#include <utility>
#include <vector>

// Mirrors the Python dict (insertion-ordered) used for INSERT/UPDATE data.
using FieldValues = std::vector<std::pair<std::string, std::string>>;

// This class generates SQL statements for common operations on a table,
// such as SELECT, INSERT, UPDATE, and DELETE.
class SQLGenerator {
public:
    // Initialize the table name.
    explicit SQLGenerator(std::string table_name)
        : table_name_(std::move(table_name)) {}

    // Generates a SELECT SQL statement based on the specified fields and
    // conditions. `fields` defaults to None ("*"); `condition` defaults to None.
    std::string select(const std::optional<std::vector<std::string>>& fields = std::nullopt,
                       const std::optional<std::string>& condition = std::nullopt) const {
        const std::string field_list =
            fields.has_value() ? join(*fields, ", ") : "*";
        std::string sql = "SELECT " + field_list + " FROM " + table_name_;
        if (condition.has_value()) {
            sql += " WHERE " + *condition;
        }
        return sql + ";";
    }

    // Generates an INSERT SQL statement based on the given data
    // (field name / field value pairs, in insertion order).
    std::string insert(const FieldValues& data) const {
        std::string fields;
        std::string values;
        for (std::size_t i = 0; i < data.size(); ++i) {
            if (i != 0) {
                fields += ", ";
                values += ", ";
            }
            fields += data[i].first;
            values += "'" + data[i].second + "'";
        }
        return "INSERT INTO " + table_name_ + " (" + fields + ") VALUES (" + values + ");";
    }

    // Generates an UPDATE SQL statement based on the given data and condition.
    std::string update(const FieldValues& data, const std::string& condition) const {
        std::string set_clause;
        for (std::size_t i = 0; i < data.size(); ++i) {
            if (i != 0) {
                set_clause += ", ";
            }
            set_clause += data[i].first + " = '" + data[i].second + "'";
        }
        return "UPDATE " + table_name_ + " SET " + set_clause + " WHERE " + condition + ";";
    }

    // Generates a DELETE SQL statement based on the given condition.
    // Named delete_ because "delete" is a reserved keyword in C++.
    std::string delete_(const std::string& condition) const {
        return "DELETE FROM " + table_name_ + " WHERE " + condition + ";";
    }

    // Generates a SQL statement to select females under a specified age.
    std::string select_female_under_age(int age) const {
        const std::string condition =
            "age < " + std::to_string(age) + " AND gender = 'female'";
        return select(std::nullopt, condition);
    }

    // Generates a SQL statement to select records within a specified age range.
    std::string select_by_age_range(int min_age, int max_age) const {
        const std::string condition =
            "age BETWEEN " + std::to_string(min_age) + " AND " + std::to_string(max_age);
        return select(std::nullopt, condition);
    }

private:
    std::string table_name_;

    static std::string join(const std::vector<std::string>& parts,
                            const std::string& separator) {
        std::string result;
        for (std::size_t i = 0; i < parts.size(); ++i) {
            if (i != 0) {
                result += separator;
            }
            result += parts[i];
        }
        return result;
    }
};