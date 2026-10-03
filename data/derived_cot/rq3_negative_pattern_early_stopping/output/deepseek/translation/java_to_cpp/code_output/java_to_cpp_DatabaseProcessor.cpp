#include <sqlite3.h>
#include <string>
#include <vector>
#include <map>
#include <variant>
#include <iostream>
#include <sstream>

class DatabaseProcessor {
private:
    std::string databaseName;

public:
    DatabaseProcessor(const std::string& databaseName) : databaseName(databaseName) {}

    void createTable(const std::string& tableName, const std::string& key1, const std::string& key2) {
        sqlite3* db;
        sqlite3_open(databaseName.c_str(), &db);
        std::string query = "CREATE TABLE IF NOT EXISTS " + tableName +
                            " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " + key2 + " INTEGER);";
        char* errMsg = nullptr;
        sqlite3_exec(db, query.c_str(), nullptr, nullptr, &errMsg);
        if (errMsg) {
            std::cerr << "SQL error: " << errMsg << std::endl;
            sqlite3_free(errMsg);
        }
        sqlite3_close(db);
    }

    void insertIntoDatabase(const std::string& tableName, const std::vector<std::map<std::string, std::variant<int, std::string>>>& data) {
        sqlite3* db;
        sqlite3_open(databaseName.c_str(), &db);
        for (const auto& item : data) {
            std::string name = std::get<std::string>(item.at("name"));
            int age = std::get<int>(item.at("age"));
            std::string query = "INSERT INTO " + tableName + " (name, age) VALUES ('" + name + "', " + std::to_string(age) + ");";
            char* errMsg = nullptr;
            sqlite3_exec(db, query.c_str(), nullptr, nullptr, &errMsg);
            if (errMsg) {
                std::cerr << "SQL error: " << errMsg << std::endl;
                sqlite3_free(errMsg);
            }
        }
        sqlite3_close(db);
    }

    std::vector<std::map<std::string, std::variant<int, std::string>>>* searchDatabase(const std::string& tableName, const std::string& name) {
        sqlite3* db;
        sqlite3_open(databaseName.c_str(), &db);
        std::string query = "SELECT * FROM " + tableName + " WHERE name = '" + name + "';";
        sqlite3_stmt* stmt;
        if (sqlite3_prepare_v2(db, query.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
            std::cerr << "SQL error: " << sqlite3_errmsg(db) << std::endl;
            sqlite3_close(db);
            return nullptr;
        }
        auto* result = new std::vector<std::map<std::string, std::variant<int, std::string>>>();
        while (sqlite3_step(stmt) == SQLITE_ROW) {
            std::map<std::string, std::variant<int, std::string>> row;
            row["id"] = sqlite3_column_int(stmt, 0);
            row["name"] = std::string(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)));
            row["age"] = sqlite3_column_int(stmt, 2);
            result->push_back(row);
        }
        sqlite3_finalize(stmt);
        sqlite3_close(db);
        if (result->empty()) {
            delete result;
            return nullptr;
        }
        return result;
    }

    void deleteFromDatabase(const std::string& tableName, const std::string& name) {
        sqlite3* db;
        sqlite3_open(databaseName.c_str(), &db);
        std::string query = "DELETE FROM " + tableName + " WHERE name = '" + name + "';";
        char* errMsg = nullptr;
        sqlite3_exec(db, query.c_str(), nullptr, nullptr, &errMsg);
        if (errMsg) {
            std::cerr << "SQL error: " << errMsg << std::endl;
            sqlite3_free(errMsg);
        }
        sqlite3_close(db);
    }
};