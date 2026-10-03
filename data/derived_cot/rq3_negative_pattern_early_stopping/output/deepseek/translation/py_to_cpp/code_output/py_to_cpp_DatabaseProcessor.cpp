#include <sqlite3.h>
#include <string>
#include <vector>
#include <tuple>
#include <optional>
#include <stdexcept>
#include <cstring>

// A simple struct representing a row (name, age) for insertion.
struct Row {
    std::string name;
    int age;
};

class DatabaseProcessor {
private:
    std::string database_name;

    // Helper to execute a query with no result (INSERT, CREATE, DELETE)
    // Returns SQLite error code on failure; throws on connection error.
    void executeNoResult(const std::string& query) {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Failed to open database: " + err);
        }

        char* errMsg = nullptr;
        rc = sqlite3_exec(db, query.c_str(), nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::string err(errMsg);
            sqlite3_free(errMsg);
            sqlite3_close(db);
            throw std::runtime_error("SQL error: " + err);
        }

        sqlite3_close(db);
    }

public:
    DatabaseProcessor(const std::string& database_name)
        : database_name(database_name) {}

    void create_table(const std::string& table_name,
                      const std::string& key1,
                      const std::string& key2) {
        std::string query = "CREATE TABLE IF NOT EXISTS " + table_name +
                            " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " +
                            key2 + " INTEGER)";
        executeNoResult(query);
    }

    void insert_into_database(const std::string& table_name,
                              const std::vector<Row>& data) {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Failed to open database: " + err);
        }

        // Use a prepared statement for efficiency (and to avoid manual quoting)
        std::string insert_query = "INSERT INTO " + table_name + " (name, age) VALUES (?, ?)";
        sqlite3_stmt* stmt = nullptr;
        rc = sqlite3_prepare_v2(db, insert_query.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Failed to prepare statement: " + err);
        }

        for (const auto& row : data) {
            // Bind values
            sqlite3_bind_text(stmt, 1, row.name.c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_bind_int(stmt, 2, row.age);

            rc = sqlite3_step(stmt);
            if (rc != SQLITE_DONE) {
                std::string err = sqlite3_errmsg(db);
                sqlite3_finalize(stmt);
                sqlite3_close(db);
                throw std::runtime_error("Insert failed: " + err);
            }

            // Reset statement for next iteration
            sqlite3_reset(stmt);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);
    }

    std::optional<std::vector<std::tuple<int, std::string, int>>>
    search_database(const std::string& table_name, const std::string& name) {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Failed to open database: " + err);
        }

        std::string select_query = "SELECT * FROM " + table_name + " WHERE name = ?";
        sqlite3_stmt* stmt = nullptr;
        rc = sqlite3_prepare_v2(db, select_query.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Failed to prepare statement: " + err);
        }

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);

        std::vector<std::tuple<int, std::string, int>> results;
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const unsigned char* nameText = sqlite3_column_text(stmt, 1);
            std::string nameStr(reinterpret_cast<const char*>(nameText));
            int age = sqlite3_column_int(stmt, 2);
            results.emplace_back(id, nameStr, age);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);

        if (results.empty()) {
            return std::nullopt;  // Mimic Python's None
        }
        return results;
    }

    void delete_from_database(const std::string& table_name,
                              const std::string& name) {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Failed to open database: " + err);
        }

        std::string delete_query = "DELETE FROM " + table_name + " WHERE name = ?";
        sqlite3_stmt* stmt = nullptr;
        rc = sqlite3_prepare_v2(db, delete_query.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Failed to prepare statement: " + err);
        }

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_finalize(stmt);
            sqlite3_close(db);
            throw std::runtime_error("Delete failed: " + err);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);
    }
};