#include <sqlite3.h>
#include <string>
#include <optional>
#include <stdexcept>

class UserLoginDB {
public:
    UserLoginDB(const std::string& db_name) {
        int rc = sqlite3_open(db_name.c_str(), &db_);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Cannot open database: " + std::string(sqlite3_errmsg(db_)));
        }
    }

    ~UserLoginDB() {
        if (db_) {
            sqlite3_close(db_);
        }
    }

    void insert_user(const std::string& username, const std::string& password) {
        sqlite3_stmt* stmt;
        const char* sql = "INSERT INTO users (username, password) VALUES (?, ?)";
        if (sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare insert statement");
        }
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, password.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to insert user");
        }
        sqlite3_finalize(stmt);
    }

    std::optional<std::pair<std::string, std::string>> search_user_by_username(const std::string& username) {
        sqlite3_stmt* stmt;
        const char* sql = "SELECT username, password FROM users WHERE username = ?";
        if (sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare search statement");
        }
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        int rc = sqlite3_step(stmt);
        if (rc == SQLITE_ROW) {
            std::string user = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0));
            std::string pass = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            sqlite3_finalize(stmt);
            return std::make_pair(user, pass);
        }
        sqlite3_finalize(stmt);
        return std::nullopt;
    }

    void delete_user_by_username(const std::string& username) {
        sqlite3_stmt* stmt;
        const char* sql = "DELETE FROM users WHERE username = ?";
        if (sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare delete statement");
        }
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to delete user");
        }
        sqlite3_finalize(stmt);
    }

    bool validate_user_login(const std::string& username, const std::string& password) {
        auto user = search_user_by_username(username);
        if (user.has_value() && user->second == password) {
            return true;
        }
        return false;
    }

private:
    sqlite3* db_ = nullptr;
};