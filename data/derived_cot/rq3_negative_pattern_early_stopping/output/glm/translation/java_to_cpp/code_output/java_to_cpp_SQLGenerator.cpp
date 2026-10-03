#include <string>
#include <vector>
#include <map>
#include <optional>

namespace org::example {

class SQLGenerator {
private:
    std::string table_name;

    // Helper equivalent to Java's String.join(delimiter, iterable)
    static std::string join(const std::vector<std::string>& v, const std::string& delimiter) {
        std::string result;
        for (size_t i = 0; i < v.size(); ++i) {
            if (i > 0) result += delimiter;
            result += v[i];
        }
        return result;
    }

    // Helper equivalent to String.join(delimiter, map.keySet())
    static std::string join_keys(const std::map<std::string, std::string>& m, const std::string& delimiter) {
        std::string result;
        bool first = true;
        for (const auto& pair : m) {
            if (!first) result += delimiter;
            result += pair.first;
            first = false;
        }
        return result;
    }

    // Helper equivalent to map.values().stream().map(v -> "'" + v + "'").collect(Collectors.joining(delimiter))
    static std::string join_values(const std::map<std::string, std::string>& m, const std::string& delimiter) {
        std::string result;
        bool first = true;
        for (const auto& pair : m) {
            if (!first) result += delimiter;
            result += "'" + pair.second + "'";
            first = false;
        }
        return result;
    }

    // Helper equivalent to map.entrySet().stream().map(e -> e.getKey() + " = '" + e.getValue() + "'").collect(Collectors.joining(delimiter))
    static std::string join_entries(const std::map<std::string, std::string>& m, const std::string& delimiter) {
        std::string result;
        bool first = true;
        for (const auto& pair : m) {
            if (!first) result += delimiter;
            result += pair.first + " = '" + pair.second + "'";
            first = false;
        }
        return result;
    }

public:
    SQLGenerator(std::string table_name) : table_name(std::move(table_name)) {}

    std::string select(const std::optional<std::vector<std::string>>& fields, const std::optional<std::string>& condition) {
        std::string fieldsStr = fields.has_value() ? join(fields.value(), ", ") : "*";
        std::string sql = "SELECT " + fieldsStr + " FROM " + table_name;
        if (condition.has_value()) {
            sql += " WHERE " + condition.value();
        }
        return sql + ";";
    }

    std::string insert(const std::map<std::string, std::string>& data) {
        // std::map is naturally sorted by key, identical to Java's TreeMap
        std::string fields = join_keys(data, ", ");
        std::string values = join_values(data, ", ");
        return "INSERT INTO " + table_name + " (" + fields + ") VALUES (" + values + ");";
    }

    std::string update(const std::map<std::string, std::string>& data, const std::string& condition) {
        std::string setClause = join_entries(data, ", ");
        return "UPDATE " + table_name + " SET " + setClause + " WHERE " + condition + ";";
    }

    // Renamed from 'delete' as it is a reserved keyword in C++
    std::string delete_(const std::string& condition) {
        return "DELETE FROM " + table_name + " WHERE " + condition + ";";
    }

    std::string selectFemaleUnderAge(int age) {
        return "SELECT * FROM " + table_name + " WHERE age < " + std::to_string(age) + " AND gender = 'female';";
    }

    std::string selectByAgeRange(int minAge, int maxAge) {
        return "SELECT * FROM " + table_name + " WHERE age BETWEEN " + std::to_string(minAge) + " AND " + std::to_string(maxAge) + ";";
    }
};

} // namespace org::example