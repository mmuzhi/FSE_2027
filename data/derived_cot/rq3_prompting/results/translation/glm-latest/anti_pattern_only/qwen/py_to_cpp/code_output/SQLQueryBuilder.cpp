#include <iostream>
#include <string>
#include <utility>
#include <vector>

/*
 * This class provides to build SQL queries, including SELECT, INSERT, UPDATE,
 * and DELETE statements.
 *
 * Note: Python dicts preserve insertion order and the generated SQL depends on
 * that order, so key/value collections are modeled with
 * std::vector<std::pair<std::string, std::string>> rather than std::map.
 * Values are strings: Python stringifies values with str() (e.g. 15 -> "15"),
 * so callers pass the equivalent string form to keep the output identical.
 */
class SQLQueryBuilder {
public:
    // Ordered key/value collection mirroring the Python dict usage.
    using Dict = std::vector<std::pair<std::string, std::string>>;

    /*
     * Generate the SELECT SQL statement from the given parameters.
     * table: the query table in the database.
     * columns: column names; the default {"*"} matches Python's default '*'.
     * where: ordered key/value pairs describing the query condition.
     * Returns the SQL query statement.
     */
    static std::string select(const std::string& table,
                              const std::vector<std::string>& columns = {"*"},
                              const Dict& where = {}) {
        std::string columnList;
        bool first = true;
        for (const std::string& column : columns) {
            if (!first) columnList += ", ";
            first = false;
            columnList += column;
        }
        std::string query = "SELECT " + columnList + " FROM " + table;
        if (!where.empty()) {
            query += " WHERE " + joinConditions(where);
        }
        return query;
    }

    /*
     * Generate the INSERT SQL statement from the given parameters.
     * table: the table to be inserted in the database.
     * data: ordered key/value pairs for the SQL insert statement.
     * Returns the SQL insert statement.
     */
    static std::string insert(const std::string& table, const Dict& data) {
        std::string keys;
        std::string values;
        bool first = true;
        for (const auto& kv : data) {
            if (!first) {
                keys += ", ";
                values += ", ";
            }
            first = false;
            keys += kv.first;
            values += "'" + kv.second + "'";
        }
        return "INSERT INTO " + table + " (" + keys + ") VALUES (" + values + ")";
    }

    /*
     * Generate the DELETE SQL statement from the given parameters.
     * table: the table that will be executed with the DELETE operation.
     * where: ordered key/value pairs describing the query condition.
     * Returns the SQL delete statement.
     * (Named delete_ because "delete" is a reserved keyword in C++.)
     */
    static std::string delete_(const std::string& table, const Dict& where = {}) {
        std::string query = "DELETE FROM " + table;
        if (!where.empty()) {
            query += " WHERE " + joinConditions(where);
        }
        return query;
    }

    /*
     * Generate the UPDATE SQL statement from the given parameters.
     * table: the table that will be executed with the UPDATE operation.
     * data: ordered key/value pairs for the SQL update statement.
     * where: ordered key/value pairs describing the query condition.
     * Returns the SQL update statement.
     */
    static std::string update(const std::string& table, const Dict& data,
                              const Dict& where = {}) {
        std::string updateStr;
        bool first = true;
        for (const auto& kv : data) {
            if (!first) updateStr += ", ";
            first = false;
            updateStr += kv.first + "='" + kv.second + "'";
        }
        std::string query = "UPDATE " + table + " SET " + updateStr;
        if (!where.empty()) {
            query += " WHERE " + joinConditions(where);
        }
        return query;
    }

private:
    // Equivalent of ' AND '.join(f"{k}='{v}'" for k, v in where.items()).
    static std::string joinConditions(const Dict& where) {
        std::string result;
        bool first = true;
        for (const auto& kv : where) {
            if (!first) result += " AND ";
            first = false;
            result += kv.first + "='" + kv.second + "'";
        }
        return result;
    }
};

int main() {
    // SQLQueryBuilder.select('table1', columns=["col1","col2"], where={"age": 15})
    std::cout << SQLQueryBuilder::select("table1", {"col1", "col2"},
                                         {{"age", "15"}})
              << '\n';

    // SQLQueryBuilder.insert('table1', {'name': 'Test', 'age': 14})
    std::cout << SQLQueryBuilder::insert("table1",
                                         {{"name", "Test"}, {"age", "14"}})
              << '\n';

    // SQLQueryBuilder.delete('table1', {'name': 'Test', 'age': 14})
    std::cout << SQLQueryBuilder::delete_("table1",
                                          {{"name", "Test"}, {"age", "14"}})
              << '\n';

    // SQLQueryBuilder.update('table1', {'name': 'Test2', 'age': 15}, where={'name': 'Test'})
    std::cout << SQLQueryBuilder::update("table1",
                                         {{"name", "Test2"}, {"age", "15"}},
                                         {{"name", "Test"}})
              << '\n';

    return 0;
}