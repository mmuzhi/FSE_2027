#include <string>
#include <optional>
#include <iostream>
#include <sqlite3.h>

class UserLoginDB {
private:
    sqlite3* connection;

    void createTable() {
        const char* createTableQuery = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)";
        sqlite3_stmt* pstmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, createTableQuery, -1, &pstmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
            return;
        }
        rc = sqlite3_step(pstmt);
        if (rc != SQLITE_DONE) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
        }
        sqlite3_finalize(pstmt);
    }

public:
    UserLoginDB(const std::string& dbName) : connection(nullptr) {
        int rc = sqlite3_open(dbName.c_str(), &connection);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
            sqlite3_close(connection);
            connection = nullptr;
            return;
        }
        createTable();
    }

    void insertUser(const std::string& username, const std::string& password) {
        const char* insertQuery = "INSERT INTO users (username, password) VALUES (?, ?)";
        sqlite3_stmt* pstmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, insertQuery, -1, &pstmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
            return;
        }
        sqlite3_bind_text(pstmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(pstmt, 2, password.c_str(), -1, SQLITE_TRANSIENT);
        rc = sqlite3_step(pstmt);
        if (rc != SQLITE_DONE) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
        }
        sqlite3_finalize(pstmt);
    }

    std::optional<std::string> searchUserByUsername(const std::string& username) {
        const char* searchQuery = "SELECT * FROM users WHERE username = ?";
        sqlite3_stmt* pstmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, searchQuery, -1, &pstmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
            return std::nullopt;
        }
        sqlite3_bind_text(pstmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        rc = sqlite3_step(pstmt);
        if (rc == SQLITE_ROW) {
            std::string result = std::string(reinterpret_cast<const char*>(sqlite3_column_text(pstmt, 0))) + "," + std::string(reinterpret_cast<const char*>(sqlite3_column_text(pstmt, 1)));
            sqlite3_finalize(pstmt);
            return result;
        } else if (rc != SQLITE_DONE) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
        }
        sqlite3_finalize(pstmt);
        return std::nullopt;
    }

    void deleteUserByUsername(const std::string& username) {
        const char* deleteQuery = "DELETE FROM users WHERE username = ?";
        sqlite3_stmt* pstmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, deleteQuery, -1, &pstmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
            return;
        }
        sqlite3_bind_text(pstmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        rc = sqlite3_step(pstmt);
        if (rc != SQLITE_DONE) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
        }
        sqlite3_finalize(pstmt);
    }

    bool validateUserLogin(const std::string& username, const std::string& password) {
        std::optional<std::string> user = searchUserByUsername(username);
        if (user.has_value()) {
            size_t commaPos = user->find(',');
            if (commaPos != std::string::npos) {
                std::string pwd = user->substr(commaPos + 1);
                return pwd == password;
            }
        }
        return false;
    }

    void close() {
        if (connection != nullptr) {
            sqlite3_close(connection);
            connection = nullptr;
        }
    }

    ~UserLoginDB() {
        close();
    }
};