#include <sqlite3.h>
#include <iostream>
#include <string>
#include <optional>
#include <vector>
#include <stdexcept>

class UserLoginDB {
private:
    sqlite3* connection;

    static std::vector<std::string> splitJava(const std::string& s, char delim) {
        std::vector<std::string> tokens;
        size_t start = 0;
        size_t end;
        bool found = false;
        while ((end = s.find(delim, start)) != std::string::npos) {
            found = true;
            tokens.push_back(s.substr(start, end - start));
            start = end + 1;
        }
        tokens.push_back(s.substr(start));
        if (found) {
            while (!tokens.empty() && tokens.back().empty()) {
                tokens.pop_back();
            }
        }
        return tokens;
    }

    void createTable() {
        if (!connection) throw std::runtime_error("Null connection");
        char* errMsg = nullptr;
        int rc = sqlite3_exec(connection,
                              "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)",
                              nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::cerr << errMsg << std::endl;
            sqlite3_free(errMsg);
        }
    }

public:
    UserLoginDB(const std::string& dbName) {
        int rc = sqlite3_open(dbName.c_str(), &connection);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errstr(rc) << std::endl;
            if (connection) sqlite3_close(connection);
            connection = nullptr;
        }
        createTable();
    }

    ~UserLoginDB() {
        close();
    }

    void insertUser(const std::string& username, const std::string& password) {
        if (!connection) throw std::runtime_error("Null connection");
        const char* sql = "INSERT INTO users (username, password) VALUES (?, ?)";
        sqlite3_stmt* stmt;
        int rc = sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
            return;
        }
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, password.c_str(), -1, SQLITE_TRANSIENT);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
        }
        sqlite3_finalize(stmt);
    }

    std::optional<std::string> searchUserByUsername(const std::string& username) {
        if (!connection) throw std::runtime_error("Null connection");
        const char* sql = "SELECT * FROM users WHERE username = ?";
        sqlite3_stmt* stmt;
        int rc = sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
            return std::nullopt;
        }
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        rc = sqlite3_step(stmt);
        if (rc == SQLITE_ROW) {
            const unsigned char* u = sqlite3_column_text(stmt, 0);
            const unsigned char* p = sqlite3_column_text(stmt, 1);
            std::string us = u ? reinterpret_cast<const char*>(u) : "null";
            std::string ps = p ? reinterpret_cast<const char*>(p) : "null";
            std::string result = us + "," + ps;
            sqlite3_finalize(stmt);
            return result;
        } else if (rc == SQLITE_DONE) {
            sqlite3_finalize(stmt);
            return std::nullopt;
        } else {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
            sqlite3_finalize(stmt);
            return std::nullopt;
        }
    }

    void deleteUserByUsername(const std::string& username) {
        if (!connection) throw std::runtime_error("Null connection");
        const char* sql = "DELETE FROM users WHERE username = ?";
        sqlite3_stmt* stmt;
        int rc = sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
            return;
        }
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::cerr << sqlite3_errmsg(connection) << std::endl;
        }
        sqlite3_finalize(stmt);
    }

    bool validateUserLogin(const std::string& username, const std::string& password) {
        auto user = searchUserByUsername(username);
        if (user.has_value()) {
            std::vector<std::string> parts = splitJava(*user, ',');
            if (parts.size() < 2) {
                throw std::out_of_range("Index 1 out of bounds for length " + std::to_string(parts.size()));
            }
            return parts[1] == password;
        }
        return false;
    }

    void close() {
        if (connection) {
            int rc = sqlite3_close(connection);
            if (rc != SQLITE_OK) {
                std::cerr << sqlite3_errmsg(connection) << std::endl;
            } else {
                connection = nullptr;
            }
        }
    }
};