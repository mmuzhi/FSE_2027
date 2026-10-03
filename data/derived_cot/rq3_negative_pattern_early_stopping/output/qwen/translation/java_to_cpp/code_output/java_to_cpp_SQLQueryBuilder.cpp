#include <vector>
#include <map>
#include <sstream>
#include <string>
#include <algorithm>

std::string split_and_join(const std::string& input, const std::string& delimiter) {
    std::vector<std::string> parts;
    if (input.empty()) {
        parts.push_back(input);
    } else {
        std::stringstream ss(input);
        std::string part;
        while (std::getline(ss, part, delimiter[0])) {
            // Trim leading and trailing whitespace
            auto start = part.find_first_not_of(" ");
            auto end = part.find_last_not_of(" ");
            if (start == std::string::npos) {
                parts.push_back("");
            } else {
                parts.push_back(part.substr(start, end - start + 1));
            }
        }
    }
    return join(parts, ",");
}

std::string join(const std::vector<std::string>& parts, const std::string& delimiter) {
    if (parts.empty()) {
        return "";
    }
    std::stringstream ss;
    for (size_t i = 0; i < parts.size(); ++i) {
        if (i > 0) {
            ss << delimiter;
        }
        ss << parts[i];
    }
    return ss.str();
}

class SQLQueryBuilder {
public:
    static std::string select(const std::string& table, const std::string& columns, const std::map<std::string, std::string>& where) {
        std::vector<std::string> columnsVec;
        if (columns.empty()) {
            columnsVec = {"*"};
        } else {
            columnsVec = split_and_join(columns, ",");
        }
        return select(table, columnsVec, where);
    }

    static std::string select(const std::string& table, const std::vector<std::string>& columns, const std::map<std::string, std::string>& where) {
        std::stringstream query;
        query << "SELECT ";
        if (!columns.empty()) {
            query << join(columns, ", ");
        } else {
            query << "*";
        }
        query << " FROM " << table;

        if (where.size() > 0) {
            query << " WHERE ";
            bool first = true;
            for (const auto& entry : where) {
                if (!first) {
                    query << " AND ";
                }
                query << entry.first << "='";
                query << entry.second;
                query << "'";
                first = false;
            }
        }
        return query.str();
    }

    static std::string insert(const std::string& table, const std::map<std::string, std::string>& data) {
        std::stringstream query;
        query << "INSERT INTO " << table << " (";
        std::stringstream values;
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

    static std::string delete_(const std::string& table, const std::map<std::string, std::string>& where) {
        std::stringstream query;
        query << "DELETE FROM " << table;
        if (!where.empty()) {
            query << " WHERE ";
            bool first = true;
            for (const auto& entry : where) {
                if (!first) {
                    query << " AND ";
                }
                query << entry.first << "='";
                query << entry.second;
                query << "'";
                first = false;
            }
        }
        return query.str();
    }

    static std::string update(const std::string& table, const std::map<std::string, std::string>& data, const std::map<std::string, std::string>& where) {
        std::stringstream query;
        query << "UPDATE " << table << " SET ";
        bool first = true;
        for (const auto& entry : data) {
            if (!first) {
                query << ", ";
            }
            query << entry.first << "='";
            query << entry.second;
            query << "'";
            first = false;
        }
        if (!where.empty()) {
            query << " WHERE ";
            bool firstWhere = true;
            for (const auto& entry : where) {
                if (!firstWhere) {
                    query << " AND ";
                }
                query << entry.first << "='";
                query << entry.second;
                query << "'";
                firstWhere = false;
            }
        }
        return query.str();
    }
};