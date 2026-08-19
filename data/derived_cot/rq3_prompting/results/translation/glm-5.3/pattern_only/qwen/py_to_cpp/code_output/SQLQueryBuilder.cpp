#include <iomanip>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

class SQLQueryBuilder {
public:
    // Ordered key/value map: preserves insertion order like a Python dict.
    // Values keep their Python str() representation (ints as digits, bools as
    // True/False, floats like str()).
    struct Value {
        std::string s;

        Value(const char* v) : s(v) {}
        Value(const std::string& v) : s(v) {}
        Value(bool v) : s(v ? "True" : "False") {}
        Value(int v) : s(std::to_string(v)) {}
        Value(long long v) : s(std::to_string(v)) {}
        Value(double v) {
            std::ostringstream oss;
            oss << v;  // default precision 6, same as str() for typical values
            s = oss.str();
            if (s.find('.') == std::string::npos) s += ".0";  // str(15.0) == "15.0"
        }
    };

    using Dict = std::vector<std::pair<std::string, Value>>;

    // select('table1')                                  -> "SELECT * FROM table1"
    // select('table1', {"col1", "col2"}, {{"age", 15}}) -> "SELECT col1, col2 FROM table1 WHERE age='15'"
    static std::string select(const std::string& table,
                              const std::vector<std::string>& columns = {},
                              const Dict& where = {}) {
        std::string cols = columns.empty() ? "*" : joinColumns(columns);
        std::string query = "SELECT " + cols + " FROM " + table;
        if (!where.empty()) {
            query += " WHERE " + whereClause(where);
        }
        return query;
    }

    // insert('table1', {{"name", "Test"}, {"age", 14}})
    //   -> "INSERT INTO table1 (name, age) VALUES ('Test', '14')"
    static std::string insert(const std::string& table, const Dict& data) {
        std::string keys, values;
        for (std::size_t i = 0; i < data.size(); ++i) {
            if (i > 0) { keys += ", "; values += ", "; }
            keys += data[i].first;
            values += "'" + data[i].second.s + "'";
        }
        return "INSERT INTO " + table + " (" + keys + ") VALUES (" + values + ")";
    }

    // delete_('table1', {{"name", "Test"}, {"age", 14}})
    //   -> "DELETE FROM table1 WHERE name='Test' AND age='14'"
    static std::string delete_(const std::string& table, const Dict& where = {}) {
        std::string query = "DELETE FROM " + table;
        if (!where.empty()) {
            query += " WHERE " + whereClause(where);
        }
        return query;
    }

    // update('table1', {{"name", "Test2"}, {"age", 15}}, {{"name", "Test"}})
    //   -> "UPDATE table1 SET name='Test2', age='15' WHERE name='Test'"
    static std::string update(const std::string& table, const Dict& data,
                              const Dict& where = {}) {
        std::string updateStr;
        for (std::size_t i = 0; i < data.size(); ++i) {
            if (i > 0) updateStr += ", ";
            updateStr += data[i].first + "='" + data[i].second.s + "'";
        }
        std::string query = "UPDATE " + table + " SET " + updateStr;
        if (!where.empty()) {
            query += " WHERE " + whereClause(where);
        }
        return query;
    }

private:
    static std::string joinColumns(const std::vector<std::string>& columns) {
        std::string result;
        for (std::size_t i = 0; i < columns.size(); ++i) {
            if (i > 0) result += ", ";
            result += columns[i];
        }
        return result;
    }

    static std::string whereClause(const Dict& where) {
        std::string result;
        for (std::size_t i = 0; i < where.size(); ++i) {
            if (i > 0) result += " AND ";
            result += where[i].first + "='" + where[i].second.s + "'";
        }
        return result;
    }
};