#ifndef DATABASE_PROCESSOR_H
#define DATABASE_PROCESSOR_H

#include <string>
#include <vector>
#include <map>
#include <variant>
#include <optional>
#include <iostream>
#include <sqlite3.h>

class DatabaseProcessor {
private:
    std::string databaseName;

    static bool driverLoaded;

public:
    using Value = std::variant<int, std::string>;
    using Row = std::map<std::string, Value>;

    DatabaseProcessor(const std::string& databaseName);
    void createTable(const std::string& tableName, const std::string& key1, const std::string& key2);
    void insertIntoDatabase(const std::string& tableName, const std::vector<Row>& data);
    std::optional<std::vector<Row>> searchDatabase(const std::string& tableName, const std::string& name);
    void deleteFromDatabase(const std::string& tableName, const std::string& name);
};

bool DatabaseProcessor::driverLoaded = []() {
    sqlite3_initialize();
    return true;
}();

DatabaseProcessor::DatabaseProcessor(const std::string& databaseName)
    : databaseName(databaseName) {}

void DatabaseProcessor::createTable(const std::string& tableName, const std::string& key1, const std::string& key2) {
    sqlite3* db = nullptr;
    int rc = sqlite3_open(databaseName.c_str(), &db);
    if (rc != SQLITE_OK) {
        std::cerr << "SQLException: " << (db ? sqlite3_errmsg(db) : "Cannot open database") << std::endl;
        if (db) sqlite3_close(db);
        return;
    }

    std::string createTableQuery = "CREATE TABLE IF NOT EXISTS " + tableName +
        " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " + key2 + " INTEGER)";

    char* errMsg = nullptr;
    rc = sqlite3_exec(db, createTableQuery.c_str(), nullptr, nullptr, &errMsg);
    if (rc != SQLITE_OK) {
        std::cerr << "SQLException: " << errMsg << std::endl;
        sqlite3_free(errMsg);
    }

    sqlite3_close(db);
}

void DatabaseProcessor::insertIntoDatabase(const std::string& tableName, const std::vector<Row>& data) {
    sqlite3* db = nullptr;
    int rc = sqlite3_open(databaseName.c_str(), &db);
    if (rc != SQLITE_OK) {
        std::cerr << "SQLException: " << (db ? sqlite3_errmsg(db) : "Cannot open database") << std::endl;
        if (db) sqlite3_close(db);
        return;
    }

    for (const auto& item : data) {
        const auto& nameVal = item.at("name");
        const auto& ageVal = item.at("age");

        std::string nameStr = std::get<std::string>(nameVal);
        int ageInt = std::get<int>(ageVal);

        std::string insertQuery = "INSERT INTO " + tableName +
            " (name, age) VALUES ('" + nameStr + "', " + std::to_string(ageInt) + ")";

        char* errMsg = nullptr;
        rc = sqlite3_exec(db, insertQuery.c_str(), nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::cerr << "SQLException: " << errMsg << std::endl;
            sqlite3_free(errMsg);
        }
    }

    sqlite3_close(db);
}

std::optional<std::vector<DatabaseProcessor::Row>> DatabaseProcessor::searchDatabase(
    const std::string& tableName, const std::string& name) {

    std::vector<Row> result;

    sqlite3* db = nullptr;
    int rc = sqlite3_open(databaseName.c_str(), &db);
    if (rc != SQLITE_OK) {
        std::cerr << "SQLException: " << (db ? sqlite3_errmsg(db) : "Cannot open database") << std::endl;
        if (db) sqlite3_close(db);
        return result.empty() ? std::nullopt : std::optional<std::vector<Row>>(std::move(result));
    }

    std::string selectQuery = "SELECT * FROM " + tableName + " WHERE name = '" + name + "'";

    sqlite3_stmt* stmt = nullptr;
    rc = sqlite3_prepare_v2(db, selectQuery.c_str(), -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        std::cerr << "SQLException: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return result.empty() ? std::nullopt : std::optional<std::vector<Row>>(std::move(result));
    }

    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        Row row;
        row["id"] = sqlite3_column_int(stmt, 0);
        const unsigned char* nameText = sqlite3_column_text(stmt, 1);
        row["name"] = nameText ? std::string(reinterpret_cast<const char*>(nameText)) : std::string();
        row["age"] = sqlite3_column_int(stmt, 2);
        result.push_back(row);
    }

    if (rc != SQLITE_DONE) {
        std::cerr << "SQLException: " << sqlite3_errmsg(db) << std::endl;
    }

    sqlite3_finalize(stmt);
    sqlite3_close(db);

    return result.empty() ? std::nullopt : std::optional<std::vector<Row>>(std::move(result));
}

void DatabaseProcessor::deleteFromDatabase(const std::string& tableName, const std::string& name) {
    sqlite3* db = nullptr;
    int rc = sqlite3_open(databaseName.c_str(), &db);
    if (rc != SQLITE_OK) {
        std::cerr << "SQLException: " << (db ? sqlite3_errmsg(db) : "Cannot open database") << std::endl;
        if (db) sqlite3_close(db);
        return;
    }

    std::string deleteQuery = "DELETE FROM " + tableName + " WHERE name = '" + name + "'";

    char* errMsg = nullptr;
    rc = sqlite3_exec(db, deleteQuery.c_str(), nullptr, nullptr, &errMsg);
    if (rc != SQLITE_OK) {
        std::cerr << "SQLException: " << errMsg << std::endl;
        sqlite3_free(errMsg);
    }

    sqlite3_close(db);
}

#endif