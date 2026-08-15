#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <utility>

class SQLGenerator {
private:
    const std::string table_name;

    static std::string join(const std::vector<std::string>& items, const std::string& delimiter) {
        std::ostringstream oss;
        for (std::size_t i = 0; i < items.size(); ++i) {
            if (i > 0) oss << delimiter;
            oss << items[i];
        }
        return oss.str();
    }

public:
    explicit SQLGenerator(std::string table_name) : table_name(std::move(table_name)) {}

    std::string select(const std::vector<std::string>* fields, const std::string* condition) const {
        std::string fieldsStr = (fields == nullptr) ? "*" : join(*fields, ", ");
        std::string sql = "SELECT " + fieldsStr + " FROM " + table_name;
        if (condition != nullptr) {
            sql += " WHERE " + *condition;
        }
        return sql + ";";
    }

    std::string insert(const std::map<std::string, std::string>& data) const {
        std::ostringstream fields;
        std::ostringstream values;
        bool first = true;
        for (const auto& entry : data) {
            if (!first) {
                fields << ", ";
                values << ", ";
            }
            fields << entry.first;
            values << "'" << entry.second << "'";
            first = false;
        }
        return "INSERT INTO " + table_name + " (" + fields.str() + ") VALUES (" + values.str() + ");";
    }

    std::string update(const std::map<std::string, std::string>& data, const std::string* condition) const {
        std::ostringstream setClause;
        bool first = true;
        for (const auto& entry : data) {
            if (!first) setClause << ", ";
            setClause << entry.first << " = '" << entry.second << "'";
            first = false;
        }
        std::string cond = (condition != nullptr) ? *condition : "null";
        return "UPDATE " + table_name + " SET " + setClause.str() + " WHERE " + cond + ";";
    }

    std::string deleteRecord(const std::string* condition) const {
        std::string cond = (condition != nullptr) ? *condition : "null";
        return "DELETE FROM " + table_name + " WHERE " + cond + ";";
    }

    std::string selectFemaleUnderAge(int age) const {
        return "SELECT * FROM " + table_name + " WHERE age < " + std::to_string(age) + " AND gender = 'female';";
    }

    std::string selectByAgeRange(int minAge, int maxAge) const {
        return "SELECT * FROM " + table_name + " WHERE age BETWEEN " + std::to_string(minAge) + " AND " + std::to_string(maxAge) + ";";
    }
};