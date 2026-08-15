#include <sqlite3.h>
#include <string>
#include <vector>
#include <optional>
#include <stdexcept>

class UserLoginDB {
public:
    explicit UserLoginDB(const std::string& db_name) {
        int rc = sqlite3_open(db_name.c_str(), &connection_);
        if (rc != SQLITE_OK) {
            std::string err = connection_ ? sqlite3_errmsg(connection_) : sqlite3_errstr(rc);
            if (connection_) sqlite3_close(connection_);
            connection_ = nullptr;
            throw std::runtime_error(err);
        }
    }

    ~UserLoginDB() {
        if (connection_) {
            sqlite3_close(connection_);
        }
    }

    UserLoginDB(const UserLoginDB&) = delete;
    UserLoginDB& operator=(const UserLoginDB&) = delete;

    void insert_user(const std::string& username, const std::string& password) {
        const char* sql = "INSERT INTO users (username, password) VALUES (?, ?)";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection_, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_bind_text(stmt, 1, username.c_str(), static_cast<int>(username.size()), SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, password.c_str(), static_cast<int>(password.size()), SQLITE_TRANSIENT);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::string err = sqlite3_errmsg(connection_);
            sqlite3_finalize(stmt);
            throw std::runtime_error(err);
        }
        sqlite3_finalize(stmt);
    }

    std::optional<std::vector<std::optional<std::string>>> search_user_by_username(const std::string& username) {
        const char* sql = "SELECT * FROM users WHERE username = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection_, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_bind_text(stmt, 1, username.c_str(), static_cast<int>(username.size()), SQLITE_TRANSIENT);
        rc = sqlite3_step(stmt);
        if (rc == SQLITE_ROW) {
            int cols = sqlite3_column_count(stmt);
            std::vector<std::optional<std::string>> row;
            row.reserve(cols);
            for (int i = 0; i < cols; ++i) {
                if (sqlite3_column_type(stmt, i) == SQLITE_NULL) {
                    row.push_back(std::nullopt);
                } else {
                    const unsigned char* text = sqlite3_column_text(stmt, i);
                    int len = sqlite3_column_bytes(stmt, i);
                    row.emplace_back(reinterpret_cast<const char*>(text), len);
                }
            }
            sqlite3_finalize(stmt);
            return row;
        }
        if (rc == SQLITE_DONE) {
            sqlite3_finalize(stmt);
            return std::nullopt;
        }
        std::string err = sqlite3_errmsg(connection_);
        sqlite3_finalize(stmt);
        throw std::runtime_error(err);
    }

    void delete_user_by_username(const std::string& username) {
        const char* sql = "DELETE FROM users WHERE username = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection_, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_bind_text(stmt, 1, username.c_str(), static_cast<int>(username.size()), SQLITE_TRANSIENT);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::string err = sqlite3_errmsg(connection_);
            sqlite3_finalize(stmt);
            throw std::runtime_error(err);
        }
        sqlite3_finalize(stmt);
    }

    bool validate_user_login(const std::string& username, const std::string& password) {
        auto user = search_user_by_username(username);
        if (user.has_value() && user->size() > 1) {
            const auto& pass_cell = (*user)[1];
            if (pass_cell.has_value() && pass_cell.value() == password) {
                return true;
            }
        }
        return false;
    }

private:
    sqlite3* connection_ = nullptr;
};