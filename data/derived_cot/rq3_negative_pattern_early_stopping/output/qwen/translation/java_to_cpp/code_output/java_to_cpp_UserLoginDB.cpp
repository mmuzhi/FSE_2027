#include <sqlite3.h>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <stdexcept>
#include <iostream>

// Forward declaration for the callback function used in C API
static int callback(void *data, int argc, char **argv, char **azColName);

class UserLoginDB {
private:
    sqlite3 *db;
    std::string dbName;

public:
    UserLoginDB(const std::string& dbName) {
        int rc = sqlite3_open(dbName.c_str(), &db);
        if (rc != SQLITE_OK) {
            fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
            sqlite3_close(db);
            db = nullptr;
        } else {
            createTable();
        }
    }

    ~UserLoginDB() {
        close();
    }

    void createTable() {
        const char *sql = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)";
        char *zErrMsg = nullptr;
        int rc = sqlite3_exec(db, sql, nullptr, nullptr, &zErrMsg);
        if (rc != SQLITE_OK) {
            fprintf(stderr, "SQL error: %s\n", zErrMsg);
            sqlite3_free(zErrMsg);
        }
    }

    void insertUser(const std::string& username, const std::string& password) {
        std::string sql = "INSERT INTO users (username, password) VALUES (?, ?)";

        // We need to use the C API for parameterized queries because the C++ SQLite wrapper doesn't have PreparedStatement.
        // Alternatively, we can use the C API directly.

        // We'll prepare the statement and bind parameters.
        sqlite3_stmt *stmt;
        const char *tail;
        int rc = sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, &tail);
        if (rc != SQLITE_OK) {
            fprintf(stderr, "Failed to prepare insert statement: %s\n", sqlite3_errmsg(db));
            return;
        }

        sqlite3_bind_text(stmt, 1, username.c_str(), username.size(), SQLITE_STATIC);
        sqlite3_bind_text(stmt, 2, password.c_str(), password.size(), SQLITE_STATIC);

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            fprintf(stderr, "Insert failed: %s\n", sqlite3_errmsg(db));
        }

        sqlite3_finalize(stmt);
    }

    std::string searchUserByUsername(const std::string& username) {
        const char *sql = "SELECT * FROM users WHERE username = ?";
        sqlite3_stmt *stmt;
        const char *tail;
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, &tail);
        if (rc != SQLITE_OK) {
            fprintf(stderr, "Failed to prepare search statement: %s\n", sqlite3_errmsg(db));
            return nullptr;
        }

        sqlite3_bind_text(stmt, 1, username.c_str(), username.size(), SQLITE_STATIC);

        std::string result;
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            const char *username_str = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0));
            const char *password_str = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            if (username_str && password_str) {
                result = std::string(username_str) + "," + std::string(password_str);
            }
        } else {
            // No row found
            sqlite3_finalize(stmt);
            return nullptr;
        }

        sqlite3_finalize(stmt);
        return result;
    }

    void deleteUserByUsername(const std::string& username) {
        std::string sql = "DELETE FROM users WHERE username = ?";
        sqlite3_stmt *stmt;
        const char *tail;
        int rc = sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, &tail);
        if (rc != SQLITE_OK) {
            fprintf(stderr, "Failed to prepare delete statement: %s\n", sqlite3_errmsg(db));
            return;
        }

        sqlite3_bind_text(stmt, 1, username.c_str(), username.size(), SQLITE_STATIC);

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            fprintf(stderr, "Delete failed: %s\n", sqlite3_errmsg(db));
        }

        sqlite3_finalize(stmt);
    }

    bool validateUserLogin(const std::string& username, const std::string& password) {
        std::string user = searchUserByUsername(username);
        if (user != nullptr) {
            // Split the string by comma
            size_t pos = user.find(',');
            if (pos != std::string::npos) {
                std::string storedPassword = user.substr(pos + 1);
                return storedPassword == password;
            }
        }
        return false;
    }

    void close() {
        if (db != nullptr) {
            int rc = sqlite3_close(db);
            // Ignore the return value because we are closing anyway.
        }
    }
};