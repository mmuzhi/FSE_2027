#include <string>
#include <vector>
#include <utility>
#include <cctype>
#include <stdexcept>

class SQLQueryBuilder {
public:
    using StringMap = std::vector<std::pair<std::string, std::string>>;

    static std::string select(const std::string& table, const char* columns, const StringMap* where);
    static std::string select(const std::string& table, const std::vector<std::string>* columns, const StringMap* where);
    static std::string insert(const std::string& table, const StringMap* data);
    static std::string deleteQuery(const std::string& table, const StringMap* where);
    static std::string update(const std::string& table, const StringMap* data, const StringMap* where);

private:
    static std::vector<std::string> splitColumns(const std::string& s);
    static std::string join(const std::vector<std::string>& v, const std::string& sep);
    static void appendWhere(std::string& query, const StringMap* where);
};

std::vector<std::string> SQLQueryBuilder::splitColumns(const std::string& s) {
    if (s.empty()) {
        return {""};
    }
    std::vector<std::string> result;
    size_t start = 0;
    while (true) {
        size_t pos = s.find(',', start);
        if (pos == std::string::npos) {
            result.push_back(s.substr(start));
            break;
        }
        result.push_back(s.substr(start, pos - start));
        size_t i = pos + 1;
        while (i < s.size() && std::isspace(static_cast<unsigned char>(s[i]))) {
            ++i;
        }
        start = i;
    }
    while (!result.empty() && result.back().empty()) {
        result.pop_back();
    }
    return result;
}

std::string SQLQueryBuilder::join(const std::vector<std::string>& v, const std::string& sep) {
    std::string result;
    for (size_t i = 0; i < v.size(); ++i) {
        if (i > 0) result += sep;
        result += v[i];
    }
    return result;
}

void SQLQueryBuilder::appendWhere(std::string& query, const StringMap* where) {
    if (where && !where->empty()) {
        query += " WHERE ";
        bool first = true;
        for (const auto& entry : *where) {
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
}

std::string SQLQueryBuilder::select(const std::string& table, const char* columns, const StringMap* where) {
    std::string cols = (columns == nullptr) ? "*" : columns;
    std::vector<std::string> split = splitColumns(cols);
    return select(table, &split, where);
}

std::string SQLQueryBuilder::select(const std::string& table, const std::vector<std::string>* columns, const StringMap* where) {
    if (!columns) {
        throw std::invalid_argument("columns is null");
    }
    std::string query = "SELECT ";
    if (!columns->empty()) {
        query += join(*columns, ", ");
    } else {
        query += "*";
    }
    query += " FROM ";
    query += table;
    appendWhere(query, where);
    return query;
}

std::string SQLQueryBuilder::insert(const std::string& table, const StringMap* data) {
    if (!data) {
        throw std::invalid_argument("data is null");
    }
    std::string query = "INSERT INTO ";
    query += table;
    query += " (";
    std::string values = " VALUES (";

    bool first = true;
    for (const auto& entry : *data) {
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

std::string SQLQueryBuilder::deleteQuery(const std::string& table, const StringMap* where) {
    std::string query = "DELETE FROM ";
    query += table;
    appendWhere(query, where);
    return query;
}

std::string SQLQueryBuilder::update(const std::string& table, const StringMap* data, const StringMap* where) {
    if (!data) {
        throw std::invalid_argument("data is null");
    }
    std::string query = "UPDATE ";
    query += table;
    query += " SET ";

    bool first = true;
    for (const auto& entry : *data) {
        if (!first) {
            query += ", ";
        }
        query += entry.first;
        query += "='";
        query += entry.second;
        query += "'";
        first = false;
    }

    appendWhere(query, where);
    return query;
}