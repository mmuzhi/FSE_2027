#include <sqlite3.h>
#include <string>
#include <iostream>
#include <optional>
#include <sstream>

class UserLoginDB {
private:
    sqlite3* connection;

    void createTable() {
        const char* createTableQuery = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)";
        sqlite3_stmt* stmt;
        int rc = sqlite3_prepare_v2(connection, createTableQuery, -1, &stmt, nullptr);
        if (rc == SQLITE_OK) {
            sqlite3_step(stmt);
            sqlite3_finalize(stmt);
        } else {
            std::cerr << "SQL error: " << sqlite3_errmsg(connection) << std::endl;
        }
    }

public:
    UserLoginDB(const std::string& dbName) : connection(nullptr) {
        int rc = sqlite3_open(dbName.c_str(), &connection);
        if (rc != SQLITE_OK) {
            std::cerr << "Can't open database: " << sqlite3_errmsg(connection) << std::endl;
            sqlite3_close(connection);
            connection = nullptr;
        } else {
            createTable();
        }
    }

    void insertUser(const std::string& username, const std::string& password) {
        const char* insertQuery = "INSERT INTO users (username, password) VALUES (?, ?)";
        sqlite3_stmt* stmt;
        int rc = sqlite3_prepare_v2(connection, insertQuery, -1, &stmt, nullptr);
        if (rc == SQLITE_OK) {
            sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_bind_text(stmt, 2, password.c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_step(stmt);
            sqlite3_finalize(stmt);
        } else {
            std::cerr << "SQL error: " << sqlite3_errmsg(connection) << std::endl;
        }
    }

    std::optional<std::string> searchUserByUsername(const std::string& username) {
        const char* searchQuery = "SELECT * FROM users WHERE username = ?";
        sqlite3_stmt* stmt;
        int rc = sqlite3_prepare_v2(connection, searchQuery, -1, &stmt, nullptr);
        if (rc == SQLITE_OK) {
            sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
            rc = sqlite3_step(stmt);
            if (rc == SQLITE_ROW) {
                const unsigned char* user = sqlite3_column_text(stmt, 0);
                const unsigned char* pass = sqlite3_column_text(stmt, 1);
                std::string result = std::string(reinterpret_cast<const char*>(user)) + "," + std::string(reinterpret_cast<const char*>(pass));
                sqlite3_finalize(stmt);
                return result;
            }
            sqlite3_finalize(stmt);
        } else {
            std::cerr << "SQL error: " << sqlite3_errmsg(connection) << std::endl;
        }
        return std::nullopt;
    }

    void deleteUserByUsername(const std::string& username) {
        const char* deleteQuery = "DELETE FROM users WHERE username = ?";
        sqlite3_stmt* stmt;
        int rc = sqlite3_prepare_v2(connection, deleteQuery, -1, &stmt, nullptr);
        if (rc == SQLITE_OK) {
            sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_step(stmt);
            sqlite3_finalize(stmt);
        } else {
            std::cerr << "SQL error: " << sqlite3_errmsg(connection) << std::endl;
        }
    }

    bool validateUserLogin(const std::string& username, const std::string& password) {
        auto user = searchUserByUsername(username);
        if (user) {
            std::string userStr = user.value();
            size_t comma = userStr.find(',');
            if (comma != std::string::npos) {
                std::string storedPassword = userStr.substr(comma + 1);
                return storedPassword == password;
            }
        }
        return false;
    }

    void close() {
        if (connection) {
            sqlite3_close(connection);
            connection = nullptr;
        }
    }
};