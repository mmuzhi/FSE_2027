#include <sqlite3.h>

#include <any>
#include <cstdio>
#include <map>
#include <optional>
#include <string>
#include <utility>
#include <vector>

namespace org::example {

class DatabaseProcessor {
private:
    std::string databaseName;

    // Java's static block loads the SQLite JDBC driver; linking the SQLite C API
    // directly requires no runtime driver load, so no equivalent is needed.

    // Equivalent of e.printStackTrace(): message on stderr, execution continues.
    static void printSQLException(const char* where, sqlite3* db) {
        std::fprintf(stderr, "java.sql.SQLException: %s\n",
                     db ? sqlite3_errmsg(db) : "unable to open database file");
        std::fprintf(stderr, "\tat org.example.DatabaseProcessor.%s(DatabaseProcessor)\n", where);
    }

    // RAII wrapper mirroring Java try-with-resources for the Connection.
    struct ScopedDb {
        sqlite3* conn = nullptr;
        explicit ScopedDb(const std::string& file) {
            if (sqlite3_open(file.c_str(), &conn) != SQLITE_OK) {
                printSQLException("getConnection", conn);
                conn = nullptr;
            }
        }
        ~ScopedDb() {
            if (conn) sqlite3_close(conn);
        }
        bool ok() const { return conn != nullptr; }
    };

    // Mirrors String.valueOf/toString semantics for String.format("%s", obj):
    // missing value renders as "null".
    static std::string anyToString(const std::any& v) {
        if (!v.has_value()) return "null";
        if (const auto* s = std::any_cast<std::string>(&v)) return *s;
        if (const auto* i = std::any_cast<int>(&v)) return std::to_string(*i);
        return "null";
    }

public:
    explicit DatabaseProcessor(std::string databaseName_)
        : databaseName(std::move(databaseName_)) {}

    void createTable(const std::string& tableName, const std::string& key1, const std::string& key2) {
        ScopedDb db(databaseName);
        if (!db.ok()) return;
        std::string createTableQuery = "CREATE TABLE IF NOT EXISTS " + tableName +
                                       " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " + key2 + " INTEGER)";
        char* err = nullptr;
        if (sqlite3_exec(db.conn, createTableQuery.c_str(), nullptr, nullptr, &err) != SQLITE_OK) {
            printSQLException("createTable", db.conn);
        }
        if (err) sqlite3_free(err);
    }

    void insertIntoDatabase(const std::string& tableName,
                            const std::vector<std::map<std::string, std::any>>& data) {
        ScopedDb db(databaseName);
        if (!db.ok()) return;
        for (const auto& item : data) {
            // (int) item.get("age") in Java throws an uncaught exception when the
            // key is missing or not an Integer; .at()/any_cast propagate likewise.
            int age = std::any_cast<int>(item.at("age"));
            std::string insertQuery = "INSERT INTO " + tableName + " (name, age) VALUES ('" +
                                      anyToString(item.at("name")) + "', " + std::to_string(age) + ")";
            char* err = nullptr;
            if (sqlite3_exec(db.conn, insertQuery.c_str(), nullptr, nullptr, &err) != SQLITE_OK) {
                printSQLException("insertIntoDatabase", db.conn);
                if (err) sqlite3_free(err);
                return; // Java's outer catch aborts the remaining loop iterations
            }
            if (err) sqlite3_free(err);
        }
    }

    // Returns nullopt where Java returns null for an empty result.
    std::optional<std::vector<std::map<std::string, std::any>>>
    searchDatabase(const std::string& tableName, const std::string& name) {
        std::vector<std::map<std::string, std::any>> result;
        ScopedDb db(databaseName);
        if (db.ok()) {
            std::string selectQuery = "SELECT * FROM " + tableName + " WHERE name = '" + name + "'";
            sqlite3_stmt* stmt = nullptr;
            if (sqlite3_prepare_v2(db.conn, selectQuery.c_str(), -1, &stmt, nullptr) == SQLITE_OK) {
                while (sqlite3_step(stmt) == SQLITE_ROW) {
                    std::map<std::string, std::any> row;
                    row.emplace("id", static_cast<int>(sqlite3_column_int(stmt, 0)));
                    const unsigned char* txt = sqlite3_column_text(stmt, 1);
                    row.emplace("name", txt ? std::string(reinterpret_cast<const char*>(txt))
                                            : std::string());
                    row.emplace("age", static_cast<int>(sqlite3_column_int(stmt, 2)));
                    result.push_back(std::move(row));
                }
                sqlite3_finalize(stmt);
            } else {
                printSQLException("searchDatabase", db.conn);
            }
        }
        if (result.empty()) return std::nullopt;
        return result;
    }

    void deleteFromDatabase(const std::string& tableName, const std::string& name) {
        ScopedDb db(databaseName);
        if (!db.ok()) return;
        std::string deleteQuery = "DELETE FROM " + tableName + " WHERE name = '" + name + "'";
        char* err = nullptr;
        if (sqlite3_exec(db.conn, deleteQuery.c_str(), nullptr, nullptr, &err) != SQLITE_OK) {
            printSQLException("deleteFromDatabase", db.conn);
        }
        if (err) sqlite3_free(err);
    }
};

} // namespace org::example