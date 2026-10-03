#ifndef SQL_QUERY_BUILDER_H
#define SQL_QUERY_BUILDER_H

#include <string>
#include <vector>
#include <sstream>
#include <regex>
#include <utility>

using OrderedMap = std::vector<std::pair<std::string, std::string>>;

class SQLQueryBuilder {
public:
    static std::string select(const std::string& table, const std::string* columns, const OrderedMap* where) {
        std::string cols = (columns != nullptr) ? *columns : "*";
        return select(table, splitColumns(cols), where);
    }

    static std::string select(const std::string& table, const std::vector<std::string>& columns, const OrderedMap* where) {
        std::string query = "SELECT ";
        if (!columns.empty()) {
            query += join(columns, ", ");
        } else {
            query += "*";
        }
        query += " FROM " + table;

        if (where != nullptr && !where->empty()) {
            query += " WHERE ";
            bool first = true;
            for (const auto& entry : *where) {
                if (!first) {
                    query += " AND ";
                }
                query += entry.first + "='" + entry.second + "'";
                first = false;
            }
        }
        return query;
    }

    static std::string insert(const std::string& table, const OrderedMap& data) {
        std::string query = "INSERT INTO " + table + " (";
        std::string values = " VALUES (";

        bool first = true;
        for (const auto& entry : data) {
            if (!first) {
                query += ", ";
                values += ", ";
            }
            query += entry.first;
            values += "'" + entry.second + "'";
            first = false;
        }

        query += ")";
        values += ")";

        return query + values;
    }

    static std::string delete_(const std::string& table, const OrderedMap* where) {
        std::string query = "DELETE FROM " + table;

        if (where != nullptr && !where->empty()) {
            query += " WHERE ";
            bool first = true;
            for (const auto& entry : *where) {
                if (!first) {
                    query += " AND ";
                }
                query += entry.first + "='" + entry.second + "'";
                first = false;
            }
        }
        return query;
    }

    static std::string update(const std::string& table, const OrderedMap& data, const OrderedMap* where) {
        std::string query = "UPDATE " + table + " SET ";

        bool first = true;
        for (const auto& entry : data) {
            if (!first) {
                query += ", ";
            }
            query += entry.first + "='" + entry.second + "'";
            first = false;
        }

        if (where != nullptr && !where->empty()) {
            query += " WHERE ";
            bool firstWhere = true;
            for (const auto& entry : *where) {
                if (!firstWhere) {
                    query += " AND ";
                }
                query += entry.first + "='" + entry.second + "'";
                firstWhere = false;
            }
        }
        return query;
    }

private:
    static std::vector<std::string> splitColumns(const std::string& columns) {
        std::vector<std::string> result;
        std::regex re(",\\s*");
        std::sregex_token_iterator it(columns.begin(), columns.end(), re, -1);
        std::sregex_token_iterator end;
        for (; it != end; ++it) {
            result.push_back(it->str());
        }
        return result;
    }

    static std::string join(const std::vector<std::string>& v, const std::string& delim) {
        std::ostringstream oss;
        bool first = true;
        for (const auto& s : v) {
            if (!first) oss << delim;
            oss << s;
            first = false;
        }
        return oss.str();
    }
};

#endif