#include <string>
#include <map>
#include <vector>
#include <sstream>

class SQLGenerator {
private:
    std::string table_name;

    // Helper function to join a vector of strings with a delimiter
    std::string join(const std::vector<std::string>& parts, const std::string& delimiter) {
        if (parts.empty()) {
            return "";
        }
        std::ostringstream oss;
        for (size_t i = 0; i < parts.size(); ++i) {
            if (i > 0) {
                oss << delimiter;
            }
            oss << parts[i];
        }
        return oss.str();
    }

public:
    SQLGenerator(const std::string& table_name) : table_name(table_name) {}

    std::string select(const std::vector<std::string>& fields, const std::string& condition = "") {
        std::vector<std::string> fieldsList;
        if (fields.empty()) {
            fieldsList = {"*"};
        } else {
            for (const auto& field : fields) {
                fieldsList.push_back(field);
            }
        }
        std::string fieldsStr = join(fieldsList, ", ");
        std::string sql = "SELECT " + fieldsStr + " FROM " + table_name;
        if (!condition.empty()) {
            sql += " WHERE " + condition;
        }
        return sql + ";";
    }

    std::string insert(const std::map<std::string, std::string>& data) {
        // We use std::map which is sorted by key
        std::vector<std::string> keys;
        for (const auto& kv : data) {
            keys.push_back(kv.first);
        }
        std::string fields = join(keys, ", ");
        std::vector<std::string> values;
        for (const auto& kv : data) {
            values.push_back("'" + kv.second + "'");
        }
        std::string valuesStr = join(values, ", ");
        return "INSERT INTO " + table_name + " (" + fields + ") VALUES (" + valuesStr + ");";
    }

    std::string update(const std::map<std::string, std::string>& data, const std::string& condition) {
        std::vector<std::string> setClauses;
        for (const auto& kv : data) {
            setClauses.push_back(kv.first + " = '" + kv.second + "'");
        }
        std::string setClause = join(setClauses, ", ");
        return "UPDATE " + table_name + " SET " + setClause + " WHERE " + condition + ";";
    }

    std::string delete_(const std::string& condition) {  // Avoid name conflict with delete operator
        return "DELETE FROM " + table_name + " WHERE " + condition + ";";
    }

    std::string selectFemaleUnderAge(int age) {
        return "SELECT * FROM " + table_name + " WHERE age < " + std::to_string(age) + " AND gender = 'female';";
    }

    std::string selectByAgeRange(int minAge, int maxAge) {
        return "SELECT * FROM " + table_name + " WHERE age BETWEEN " + std::to_string(minAge) + " AND " + std::to_string(maxAge) + ";";
    }
};