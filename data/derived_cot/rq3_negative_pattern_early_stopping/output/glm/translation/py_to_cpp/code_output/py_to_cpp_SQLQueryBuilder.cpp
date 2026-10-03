#include <string>
#include <vector>
#include <sstream>
#include <optional>

class SQLQueryBuilder {
public:
    static std::string select(
        const std::string& table,
        const std::optional<std::vector<std::string>>& columns = std::nullopt,
        const std::optional<std::vector<std::pair<std::string, std::string>>>& where = std::nullopt
    ) {
        std::string cols_str = "*";
        if (columns.has_value()) {
            std::ostringstream oss;
            for (size_t i = 0; i < columns->size(); ++i) {
                if (i > 0) oss << ", ";
                oss << (*columns)[i];
            }
            cols_str = oss.str();
        }
        std::string query = "SELECT " + cols_str + " FROM " + table;
        if (where.has_value() && !where->empty()) {
            query += " WHERE ";
            for (size_t i = 0; i < where->size(); ++i) {
                if (i > 0) query += " AND ";
                query += (*where)[i].first + "='" + (*where)[i].second + "'";
            }
        }
        return query;
    }

    static std::string insert(
        const std::string& table,
        const std::vector<std::pair<std::string, std::string>>& data
    ) {
        std::ostringstream keys_oss, values_oss;
        for (size_t i = 0; i < data.size(); ++i) {
            if (i > 0) {
                keys_oss << ", ";
                values_oss << ", ";
            }
            keys_oss << data[i].first;
            values_oss << "'" << data[i].second << "'";
        }
        return "INSERT INTO " + table + " (" + keys_oss.str() + ") VALUES (" + values_oss.str() + ")";
    }

    static std::string delete_(
        const std::string& table,
        const std::optional<std::vector<std::pair<std::string, std::string>>>& where = std::nullopt
    ) {
        std::string query = "DELETE FROM " + table;
        if (where.has_value() && !where->empty()) {
            query += " WHERE ";
            for (size_t i = 0; i < where->size(); ++i) {
                if (i > 0) query += " AND ";
                query += (*where)[i].first + "='" + (*where)[i].second + "'";
            }
        }
        return query;
    }

    static std::string update(
        const std::string& table,
        const std::vector<std::pair<std::string, std::string>>& data,
        const std::optional<std::vector<std::pair<std::string, std::string>>>& where = std::nullopt
    ) {
        std::ostringstream update_oss;
        for (size_t i = 0; i < data.size(); ++i) {
            if (i > 0) update_oss << ", ";
            update_oss << data[i].first << "='" << data[i].second << "'";
        }
        std::string query = "UPDATE " + table + " SET " + update_oss.str();
        if (where.has_value() && !where->empty()) {
            query += " WHERE ";
            for (size_t i = 0; i < where->size(); ++i) {
                if (i > 0) query += " AND ";
                query += (*where)[i].first + "='" + (*where)[i].second + "'";
            }
        }
        return query;
    }
};