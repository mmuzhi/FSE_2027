#include <cctype>
#include <string>
#include <utility>
#include <vector>

namespace org {
namespace example {

// Insertion-ordered stand-in for Map<String,String> (LinkedHashMap semantics).
using StringMap = std::vector<std::pair<std::string, std::string>>;

namespace {

// Equivalent of Java's columns.split(",\\s*"):
// delimiter = ',' followed by any run of whitespace; trailing empty tokens are
// dropped; empty/blank input yields a single empty token (Java split semantics).
std::vector<std::string> SplitColumns(const std::string& columns) {
    std::vector<std::string> parts;
    std::string current;
    std::size_t i = 0;
    while (i < columns.size()) {
        if (columns[i] == ',') {
            parts.push_back(current);
            current.clear();
            ++i;
            while (i < columns.size() &&
                   std::isspace(static_cast<unsigned char>(columns[i]))) {
                ++i;
            }
        } else {
            current += columns[i++];
        }
    }
    parts.push_back(current);
    while (!parts.empty() && parts.back().empty()) {
        parts.pop_back();
    }
    if (parts.empty()) {
        parts.emplace_back();
    }
    return parts;
}

void AppendWhere(std::string& query, const StringMap& where) {
    query += " WHERE ";
    bool first = true;
    for (const auto& entry : where) {
        if (!first) {
            query += " AND ";
        }
        query += entry.first;
        query += "='";
        query += entry.second;
        query += "'";
        first = false;
    }
}

}  // namespace

struct SQLQueryBuilder {
    // Note: `delete` is a C++ keyword, hence `Delete`.

    static std::string Select(const std::string& table, const char* columns,
                              const StringMap* where) {
        if (columns == nullptr) {
            columns = "*";
        }
        return Select(table, SplitColumns(columns), where);
    }

    static std::string Select(const std::string& table,
                              const std::vector<std::string>& columns,
                              const StringMap* where) {
        std::string query = "SELECT ";
        if (!columns.empty()) {
            for (std::size_t i = 0; i < columns.size(); ++i) {
                if (i > 0) {
                    query += ", ";
                }
                query += columns[i];
            }
        } else {
            query += "*";
        }
        query += " FROM ";
        query += table;

        if (where != nullptr && !where->empty()) {
            AppendWhere(query, *where);
        }
        return query;
    }

    static std::string Insert(const std::string& table, const StringMap& data) {
        std::string query = "INSERT INTO ";
        query += table;
        query += " (";
        std::string values = " VALUES (";

        bool first = true;
        for (const auto& entry : data) {
            if (!first) {
                query += ", ";
                values += ", ";
            }
            query += entry.first;
            values += "'";
            values += entry.second;
            values += "'";
            first = false;
        }

        query += ")";
        values += ")";

        query += values;
        return query;
    }

    static std::string Delete(const std::string& table, const StringMap* where) {
        std::string query = "DELETE FROM ";
        query += table;

        if (where != nullptr && !where->empty()) {
            AppendWhere(query, *where);
        }
        return query;
    }

    static std::string Update(const std::string& table, const StringMap& data,
                              const StringMap* where) {
        std::string query = "UPDATE ";
        query += table;
        query += " SET ";

        bool first = true;
        for (const auto& entry : data) {
            if (!first) {
                query += ", ";
            }
            query += entry.first;
            query += "='";
            query += entry.second;
            query += "'";
            first = false;
        }

        if (where != nullptr && !where->empty()) {
            AppendWhere(query, *where);
        }
        return query;
    }
};

}  // namespace example
}  // namespace org