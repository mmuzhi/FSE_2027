#include <cstddef>
#include <map>
#include <optional>
#include <string>
#include <utility>
#include <vector>

namespace org::example {

class SQLGenerator {
private:
    std::string table_name;

    static std::string join(const std::vector<std::string>& parts, const std::string& delimiter) {
        std::string result;
        for (std::size_t i = 0; i < parts.size(); ++i) {
            if (i > 0) {
                result += delimiter;
            }
            result += parts[i];
        }
        return result;
    }

public:
    explicit SQLGenerator(std::string table_name) : table_name(std::move(table_name)) {}

    // Java's null for 'fields'/'condition' is represented by std::nullopt.
    std::string select(const std::optional<std::vector<std::string>>& fields,
                       const std::optional<std::string>& condition) const {
        std::string fieldsStr = fields.has_value() ? join(*fields, ", ") : "*";
        std::string sql = "SELECT " + fieldsStr + " FROM " + table_name;
        if (condition.has_value()) {
            sql += " WHERE " + *condition;
        }
        return sql + ";";
    }

    // std::map iterates in sorted key order, matching Java's TreeMap copy.
    std::string insert(const std::map<std::string, std::string>& data) const {
        std::string fields;
        std::string values;
        bool first = true;
        for (const auto& entry : data) {
            if (!first) {
                fields += ", ";
                values += ", ";
            }
            first = false;
            fields += entry.first;
            values += "'" + entry.second + "'";
        }
        return "INSERT INTO " + table_name + " (" + fields + ") VALUES (" + values + ");";
    }

    std::string update(const std::map<std::string, std::string>& data, const std::string& condition) const {
        std::string setClause;
        bool first = true;
        for (const auto& entry : data) {
            if (!first) {
                setClause += ", ";
            }
            first = false;
            setClause += entry.first + " = '" + entry.second + "'";
        }
        return "UPDATE " + table_name + " SET " + setClause + " WHERE " + condition + ";";
    }

    // Named delete_ because 'delete' is a reserved keyword in C++.
    std::string delete_(const std::string& condition) const {
        return "DELETE FROM " + table_name + " WHERE " + condition + ";";
    }

    std::string selectFemaleUnderAge(int age) const {
        return "SELECT * FROM " + table_name + " WHERE age < " + std::to_string(age) +
               " AND gender = 'female';";
    }

    std::string selectByAgeRange(int minAge, int maxAge) const {
        return "SELECT * FROM " + table_name + " WHERE age BETWEEN " + std::to_string(minAge) +
               " AND " + std::to_string(maxAge) + ";";
    }
};

}  // namespace org::example