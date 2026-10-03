#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <algorithm>
#include <iterator>

class SQLQueryBuilder {
public:
    // Select: columns can be "*" (default) or a vector of column names.
    static std::string select(const std::string& table,
                              const std::string& columns = "*",
                              const std::map<std::string, std::string>& where = {}) {
        std::string query = "SELECT ";
        if (columns == "*") {
            query += "*";
        } else {
            // columns is a single column name? The Python version expects a list.
            // This overload is kept for the case where a single string is passed,
            // but externally the vector overload will be used for multiple columns.
            query += columns;
        }
        query += " FROM " + table;
        if (!where.empty()) {
            query += " WHERE " + joinWhere(where);
        }
        return query;
    }

    // Overload for vector of column names.
    static std::string select(const std::string& table,
                              const std::vector<std::string>& columns,
                              const std::map<std::string, std::string>& where = {}) {
        std::string query = "SELECT " + join(columns, ", ") + " FROM " + table;
        if (!where.empty()) {
            query += " WHERE " + joinWhere(where);
        }
        return query;
    }

    static std::string insert(const std::string& table,
                              const std::map<std::string, std::string>& data) {
        std::string keys = joinKeys(data);
        std::string values = joinValues(data);
        return "INSERT INTO " + table + " (" + keys + ") VALUES (" + values + ")";
    }

    static std::string delete_(const std::string& table,
                               const std::map<std::string, std::string>& where = {}) {
        std::string query = "DELETE FROM " + table;
        if (!where.empty()) {
            query += " WHERE " + joinWhere(where);
        }
        return query;
    }

    static std::string update(const std::string& table,
                              const std::map<std::string, std::string>& data,
                              const std::map<std::string, std::string>& where = {}) {
        std::string setClause = joinSetClause(data);
        std::string query = "UPDATE " + table + " SET " + setClause;
        if (!where.empty()) {
            query += " WHERE " + joinWhere(where);
        }
        return query;
    }

private:
    // Join a sequence with a delimiter.
    template<typename Iter>
    static std::string join(Iter begin, Iter end, const std::string& delimiter) {
        std::ostringstream oss;
        if (begin != end) {
            oss << *begin;
            ++begin;
        }
        for (; begin != end; ++begin) {
            oss << delimiter << *begin;
        }
        return oss.str();
    }

    static std::string join(const std::vector<std::string>& vec, const std::string& delimiter) {
        return join(vec.begin(), vec.end(), delimiter);
    }

    // Join keys of a map with ", " for INSERT.
    static std::string joinKeys(const std::map<std::string, std::string>& m) {
        std::vector<std::string> keys;
        keys.reserve(m.size());
        for (const auto& pair : m) {
            keys.push_back(pair.first);
        }
        return join(keys, ", ");
    }

    // Join values of a map with ", " for INSERT, quoting each value.
    static std::string joinValues(const std::map<std::string, std::string>& m) {
        std::vector<std::string> values;
        values.reserve(m.size());
        for (const auto& pair : m) {
            values.push_back("'" + pair.second + "'");
        }
        return join(values, ", ");
    }

    // Join key='value' pairs for WHERE clause with " AND ".
    static std::string joinWhere(const std::map<std::string, std::string>& m) {
        std::vector<std::string> conditions;
        conditions.reserve(m.size());
        for (const auto& pair : m) {
            conditions.push_back(pair.first + "='" + pair.second + "'");
        }
        return join(conditions, " AND ");
    }

    // Join key='value' pairs for SET clause with ", ".
    static std::string joinSetClause(const std::map<std::string, std::string>& m) {
        // SET uses the same format as WHERE but separated by commas.
        std::vector<std::string> assignments;
        assignments.reserve(m.size());
        for (const auto& pair : m) {
            assignments.push_back(pair.first + "='" + pair.second + "'");
        }
        return join(assignments, ", ");
    }
};