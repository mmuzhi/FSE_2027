#include <sqlite3.h>
#include <string>
#include <vector>
#include <map>
#include <any>
#include <optional>
#include <iostream>
#include <utility>

class DatabaseProcessor {
public:
    DatabaseProcessor(const std::string& databaseName) : databaseName(databaseName) {}

    void createTable(const std::string& tableName, const std::string& key1, const std::string& key2) {
        sqlite3* conn = nullptr;
        int rc = sqlite3_open(databaseName.c_str(), &conn);
        if (rc != SQLITE_OK) {
            std::cerr << "SQLException: " << sqlite3_errmsg(conn) << std::endl;
            if (conn) sqlite3_close(conn);
            return;
        }

        std::string query = "CREATE TABLE IF NOT EXISTS " + tableName +
                            " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " + key2 + " INTEGER)";
        char* errMsg = nullptr;
        if (sqlite3_exec(conn, query.c_str(), nullptr, nullptr, &errMsg) != SQLITE_OK) {
            std::cerr << "SQLException: " << (errMsg ? errMsg : "unknown error") << std::endl;
            sqlite3_free(errMsg);
        }
        sqlite3_close(conn);
    }

    void insertIntoDatabase(const std::string& tableName,
                            const std::vector<std::map<std::string, std::any>>& data) {
        sqlite3* conn = nullptr;
        int rc = sqlite3_open(databaseName.c_str(), &conn);
        if (rc != SQLITE_OK) {
            std::cerr << "SQLException: " << sqlite3_errmsg(conn) << std::endl;
            if (conn) sqlite3_close(conn);
            return;
        }

        for (const auto& item : data) {
            try {
                std::string name = std::any_cast<std::string>(item.at("name"));
                int age = std::any_cast<int>(item.at("age"));
                std::string query = "INSERT INTO " + tableName + " (name, age) VALUES ('" +
                                    name + "', " + std::to_string(age) + ")";
                char* errMsg = nullptr;
                if (sqlite3_exec(conn, query.c_str(), nullptr, nullptr, &errMsg) != SQLITE_OK) {
                    std::cerr << "SQLException: " << (errMsg ? errMsg : "unknown error") << std::endl;
                    sqlite3_free(errMsg);
                    break;
                }
            } catch (const std::bad_any_cast&) {
                sqlite3_close(conn);
                throw;
            }
        }
        sqlite3_close(conn);
    }

    std::optional<std::vector<std::map<std::string, std::any>>> searchDatabase(
            const std::string& tableName, const std::string& name) {
        std::vector<std::map<std::string, std::any>> result;
        sqlite3* conn = nullptr;
        int rc = sqlite3_open(databaseName.c_str(), &conn);
        if (rc != SQLITE_OK) {
            std::cerr << "SQLException: " << sqlite3_errmsg(conn) << std::endl;
            if (conn) sqlite3_close(conn);
            return std::nullopt;
        }

        std::string query = "SELECT * FROM " + tableName + " WHERE name = '" + name + "'";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(conn, query.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
            std::cerr << "SQLException: " << sqlite3_errmsg(conn) << std::endl;
            sqlite3_close(conn);
            return std::nullopt;
        }

        bool error = false;
        while (true) {
            int stepResult = sqlite3_step(stmt);
            if (stepResult == SQLITE_ROW) {
                std::map<std::string, std::any> row;
                row["id"] = sqlite3_column_int(stmt, 0);
                row["name"] = std::string(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)));
                row["age"] = sqlite3_column_int(stmt, 2);
                result.push_back(std::move(row));
            } else if (stepResult == SQLITE_DONE) {
                break;
            } else {
                std::cerr << "SQLException: " << sqlite3_errmsg(conn) << std::endl;
                error = true;
                break;
            }
        }

        sqlite3_finalize(stmt);
        sqlite3_close(conn);

        if (error) return std::nullopt;
        if (result.empty()) return std::nullopt;
        return result;
    }

    void deleteFromDatabase(const std::string& tableName, const std::string& name) {
        sqlite3* conn = nullptr;
        int rc = sqlite3_open(databaseName.c_str(), &conn);
        if (rc != SQLITE_OK) {
            std::cerr << "SQLException: " << sqlite3_errmsg(conn) << std::endl;
            if (conn) sqlite3_close(conn);
            return;
        }

        std::string query = "DELETE FROM " + tableName + " WHERE name = '" + name + "'";
        char* errMsg = nullptr;
        if (sqlite3_exec(conn, query.c_str(), nullptr, nullptr, &errMsg) != SQLITE_OK) {
            std::cerr << "SQLException: " << (errMsg ? errMsg : "unknown error") << std::endl;
            sqlite3_free(errMsg);
        }
        sqlite3_close(conn);
    }

private:
    std::string databaseName;
};