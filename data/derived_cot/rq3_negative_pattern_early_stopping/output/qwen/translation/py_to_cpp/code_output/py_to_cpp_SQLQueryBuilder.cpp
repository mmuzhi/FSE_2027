#include <string>
#include <vector>
#include <map>
#include <optional>

class SQLQueryBuilder {
public:
    static std::string select(const std::string& table, const std::optional<std::vector<std::string>>& columns = std::nullopt, const std::optional<std::map<std::string, std::string>>& where = std::nullopt) {
        std::string columns_str;
        if (!columns) {
            columns_str = "*";
        } else {
            if (columns->empty()) {
                columns_str = "*";
            } else {
                for (size_t i = 0; i < columns->size(); ++i) {
                    if (i > 0) {
                        columns_str += ", ";
                    }
                    columns_str += (*columns)[i];
                }
            }
        }
        std::string query = "SELECT " + columns_str + " FROM " + table;
        if (where) {
            std::string conditions;
            for (const auto& [key, value] : *where) {
                if (!conditions.empty()) {
                    conditions += " AND ";
                } else {
                    conditions += "WHERE ";
                }
                conditions += key + "='" + value + "'";
            }
            query += " " + conditions;
        }
        return query;
    }

    static std::string insert(const std::string& table, const std::map<std::string, std::string>& data) {
        std::string keys;
        for (size_t i = 0; i < data.size(); ++i) {
            if (i > 0) {
                keys += ", ";
            }
            keys += (i < data.size() ? (*data.begin())[i] : "");
        }
        std::string values;
        for (const auto& [key, value] : data) {
            if (!values.empty()) {
                values += ", ";
            }
            values += "'" + value + "'";
        }
        return "INSERT INTO " + table + " (" + keys + ") VALUES (" + values + ")";
    }

    static std::string delete_(const std::string& table, const std::optional<std::map<std::string, std::string>>& where = std::nullopt) {
        std::string query = "DELETE FROM " + table;
        if (where) {
            std::string conditions;
            for (const auto& [key, value] : *where) {
                if (!conditions.empty()) {
                    conditions += " AND ";
                } else {
                    conditions += "WHERE ";
                }
                conditions += key + "='" + value + "'";
            }
            query += " " + conditions;
        }
        return query;
    }

    static std::string update(const std::string& table, const std::map<std::string, std::string>& data, const std::optional<std::map<std::string, std::string>>& where = std::nullopt) {
        std::string update_str;
        for (const auto& [key, value] : data) {
            if (!update_str.empty()) {
                update_str += ", ";
            }
            update_str += key + "='" + value + "'";
        }
        std::string query = "UPDATE " + table + " SET " + update_str;
        if (where) {
            std::string conditions;
            for (const auto& [key, value] : *where) {
                if (!conditions.empty()) {
                    conditions += " AND ";
                } else {
                    conditions += "WHERE ";
                }
                conditions += key + "='" + value + "'";
            }
            query += " " + conditions;
        }
        return query;
    }
};