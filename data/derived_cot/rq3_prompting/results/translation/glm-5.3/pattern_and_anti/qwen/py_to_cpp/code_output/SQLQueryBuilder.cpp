#include <string>
#include <utility>
#include <vector>

class SQLQueryBuilder {
public:
    // Mirrors Python dict (insertion order preserved) with str keys/values.
    using Dict = std::vector<std::pair<std::string, std::string>>;

    static std::string select(const std::string& table,
                              const std::string& columns = "*",
                              const Dict& where = {}) {
        std::string query = "SELECT " + columns + " FROM " + table;
        if (!where.empty()) {
            query += " WHERE " + joinConditions(where);
        }
        return query;
    }

    // Overload for columns given as a list of column names.
    static std::string select(const std::string& table,
                              const std::vector<std::string>& columns,
                              const Dict& where = {}) {
        std::string cols;
        for (std::size_t i = 0; i < columns.size(); ++i) {
            if (i) cols += ", ";
            cols += columns[i];
        }
        return select(table, cols, where);
    }

    static std::string insert(const std::string& table, const Dict& data) {
        std::string keys, values;
        for (std::size_t i = 0; i < data.size(); ++i) {
            if (i) { keys += ", "; values += ", "; }
            keys += data[i].first;
            values += "'" + data[i].second + "'";
        }
        return "INSERT INTO " + table + " (" + keys + ") VALUES (" + values + ")";
    }

    // Named delete_ because "delete" is a reserved keyword in C++.
    static std::string delete_(const std::string& table, const Dict& where = {}) {
        std::string query = "DELETE FROM " + table;
        if (!where.empty()) {
            query += " WHERE " + joinConditions(where);
        }
        return query;
    }

    static std::string update(const std::string& table, const Dict& data, const Dict& where = {}) {
        std::string updateStr;
        for (std::size_t i = 0; i < data.size(); ++i) {
            if (i) updateStr += ", ";
            updateStr += data[i].first + "='" + data[i].second + "'";
        }
        std::string query = "UPDATE " + table + " SET " + updateStr;
        if (!where.empty()) {
            query += " WHERE " + joinConditions(where);
        }
        return query;
    }

private:
    static std::string joinConditions(const Dict& where) {
        std::string result;
        for (std::size_t i = 0; i < where.size(); ++i) {
            if (i) result += " AND ";
            result += where[i].first + "='" + where[i].second + "'";
        }
        return result;
    }
};