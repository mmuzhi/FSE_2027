#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <algorithm>

class SQLGenerator {
private:
    std::string table_name;

    static std::string join(const std::vector<std::string>& parts, const std::string& delimiter) {
        std::ostringstream oss;
        for (size_t i = 0; i < parts.size(); ++i) {
            if (i > 0) oss << delimiter;
            oss << parts[i];
        }
        return oss.str();
    }

    static std::vector<std::string> quoteValues(const std::vector<std::string>& values) {
        std::vector<std::string> quoted;
        quoted.reserve(values.size());
        for (const auto& v : values) {
            quoted.push_back("'" + v + "'");
        }
        return quoted;
    }

public:
    SQLGenerator(const std::string& table_name) : table_name(table_name) {}

    std::string select(const std::vector<std::string>* fields, const std::string* condition) {
        std::string fieldsStr;
        if (fields == nullptr) {
            fieldsStr = "*";
        } else {
            fieldsStr = join(*fields, ", ");
        }
        std::string sql = "SELECT " + fieldsStr + " FROM " + table_name;
        if (condition != nullptr) {
            sql += " WHERE " + *condition;
        }
        return sql + ";";
    }

    std::string insert(const std::map<std::string, std::string>& data) {
        // TreeMap in Java orders by key; std::map is already ordered.
        std::vector<std::string> keys;
        std::vector<std::string> values;
        for (const auto& pair : data) {
            keys.push_back(pair.first);
            values.push_back(pair.second);
        }
        std::string fields = join(keys, ", ");
        std::string quotedValues = join(quoteValues(values), ", ");
        return "INSERT INTO " + table_name + " (" + fields + ") VALUES (" + quotedValues + ");";
    }

    std::string update(const std::map<std::string, std::string>& data, const std::string& condition) {
        std::vector<std::string> setClauses;
        for (const auto& pair : data) {
            setClauses.push_back(pair.first + " = '" + pair.second + "'");
        }
        std::string setClause = join(setClauses, ", ");
        return "UPDATE " + table_name + " SET " + setClause + " WHERE " + condition + ";";
    }

    std::string delete(const std::string& condition) {
        return "DELETE FROM " + table_name + " WHERE " + condition + ";";
    }

    std::string selectFemaleUnderAge(int age) {
        return "SELECT * FROM " + table_name + " WHERE age < " + std::to_string(age) + " AND gender = 'female';";
    }

    std::string selectByAgeRange(int minAge, int maxAge) {
        return "SELECT * FROM " + table_name + " WHERE age BETWEEN " + std::to_string(minAge) + " AND " + std::to_string(maxAge) + ";";
    }
};