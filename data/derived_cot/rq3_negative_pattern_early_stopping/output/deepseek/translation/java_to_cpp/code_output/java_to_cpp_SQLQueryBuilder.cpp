#include <string>
#include <vector>
#include <map>
#include <sstream>

namespace org { namespace example {

class SQLQueryBuilder {
public:
    // Use std::vector<std::pair<std::string, std::string>> to preserve insertion order (like LinkedHashMap)
    using StringMap = std::vector<std::pair<std::string, std::string>>;

    static std::string select(const std::string& table, const std::string& columns, const StringMap& where) {
        std::string cols = columns.empty() ? "*" : columns;
        // split by ",\\s*" using regex or manual; manual split to avoid regex dependency
        std::vector<std::string> colArray;
        size_t start = 0, end;
        while ((end = cols.find(", ", start)) != std::string::npos) {
            std::string token = cols.substr(start, end - start);
            // remove trailing whitespace? The regex ", " matches comma+space. We'll handle by trimming? Simpler: just split by ',' then trim whitespace.
            // Actually the Java split regex is ",\s*" which means comma followed by zero or more whitespace.
            // We'll implement similar behavior: split by comma, then trim leading whitespace from each part.
            token = cols.substr(start, end - start);
            // trim leading whitespace (but the split will have no leading spaces because we split on comma-space? Not guaranteed.)
            // Better to split by comma then trim each.
            colArray.push_back(trim(token));
            start = end + 2; // skip comma and space? If only comma? Not robust.
        }
        // Actually let's do proper split with regex? We'll implement manual split by ',', then trim leading/trailing whitespace.
        // To keep it simple and avoid regex, we'll do a simple split on ',' and then trim whitespace.
        colArray = splitAndTrim(cols, ',');
        return select(table, colArray, where);
    }

    static std::string select(const std::string& table, const std::vector<std::string>& columns, const StringMap& where) {
        std::ostringstream query;
        query << "SELECT ";
        if (!columns.empty()) {
            bool first = true;
            for (const auto& col : columns) {
                if (!first) query << ", ";
                query << col;
                first = false;
            }
        } else {
            query << "*";
        }
        query << " FROM " << table;

        if (!where.empty()) {
            query << " WHERE ";
            bool first = true;
            for (const auto& entry : where) {
                if (!first) query << " AND ";
                query << entry.first << "='" << entry.second << "'";
                first = false;
            }
        }
        return query.str();
    }

    static std::string insert(const std::string& table, const StringMap& data) {
        std::ostringstream query, values;
        query << "INSERT INTO " << table << " (";
        values << " VALUES (";

        bool first = true;
        for (const auto& entry : data) {
            if (!first) {
                query << ", ";
                values << ", ";
            }
            query << entry.first;
            values << "'" << entry.second << "'";
            first = false;
        }

        query << ")";
        values << ")";
        return query.str() + values.str();
    }

    static std::string deleteRecord(const std::string& table, const StringMap& where) {
        std::ostringstream query;
        query << "DELETE FROM " << table;

        if (!where.empty()) {
            query << " WHERE ";
            bool first = true;
            for (const auto& entry : where) {
                if (!first) query << " AND ";
                query << entry.first << "='" << entry.second << "'";
                first = false;
            }
        }
        return query.str();
    }

    static std::string update(const std::string& table, const StringMap& data, const StringMap& where) {
        std::ostringstream query;
        query << "UPDATE " << table << " SET ";

        bool first = true;
        for (const auto& entry : data) {
            if (!first) query << ", ";
            query << entry.first << "='" << entry.second << "'";
            first = false;
        }

        if (!where.empty()) {
            query << " WHERE ";
            bool firstWhere = true;
            for (const auto& entry : where) {
                if (!firstWhere) query << " AND ";
                query << entry.first << "='" << entry.second << "'";
                firstWhere = false;
            }
        }
        return query.str();
    }

private:
    // Helper to split string by delimiter, trim whitespace from each token
    static std::vector<std::string> splitAndTrim(const std::string& str, char delimiter) {
        std::vector<std::string> tokens;
        std::string token;
        std::istringstream tokenStream(str);
        while (std::getline(tokenStream, token, delimiter)) {
            // trim leading and trailing whitespace
            size_t start = token.find_first_not_of(" \t\n\r\f\v");
            size_t end = token.find_last_not_of(" \t\n\r\f\v");
            if (start != std::string::npos) {
                tokens.push_back(token.substr(start, end - start + 1));
            }
        }
        return tokens;
    }

    static std::string trim(const std::string& s) {
        // simple trim (not fully but okay for now, or use above)
        size_t start = s.find_first_not_of(" \t\n\r\f\v");
        size_t end = s.find_last_not_of(" \t\n\r\f\v");
        if (start == std::string::npos) return "";
        return s.substr(start, end - start + 1);
    }
};

}} // namespace org::example