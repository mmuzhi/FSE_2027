#include <sqlite3.h>
#include <string>
#include <vector>
#include <optional>
#include <stdexcept>
#include <utility>

// Database management class for user login verification: insert user info,
// search user info, delete user info, and validate user login.
class UserLoginDB {
public:
    explicit UserLoginDB(const std::string& db_name) {
        // Equivalent of sqlite3.connect(db_name); raises on failure.
        if (sqlite3_open(db_name.c_str(), &connection_) != SQLITE_OK) {
            std::string msg = connection_ ? sqlite3_errmsg(connection_)
                                          : "unable to open database file";
            sqlite3_close(connection_);
            connection_ = nullptr;
            throw std::runtime_error(msg);
        }
    }

    // Non-copyable (owns the connection handle).
    UserLoginDB(const UserLoginDB&) = delete;
    UserLoginDB& operator=(const UserLoginDB&) = delete;

    // Inserts a new user into the "users" table.
    void insert_user(const std::string& username, const std::string& password) {
        const char* sql =
            "INSERT INTO users (username, password) VALUES (?, ?)";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection_, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, password.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_finalize(stmt);
        // Python commits explicitly; in SQLite autocommit mode the statement
        // is already durably committed, so no separate COMMIT is needed.
    }

    // Searches for a user in the "users" table by username.
    // Returns the matching row, or std::nullopt when no row matches
    // (equivalent of fetchone() returning None).
    std::optional<std::vector<std::string>>
    search_user_by_username(const std::string& username) {
        const char* sql = "SELECT * FROM users WHERE username = ?";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection_, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);

        std::optional<std::vector<std::string>> user;
        int rc = sqlite3_step(stmt);
        if (rc == SQLITE_ROW) {
            int cols = sqlite3_column_count(stmt);
            std::vector<std::string> row;
            row.reserve(static_cast<std::size_t>(cols));
            for (int i = 0; i < cols; ++i) {
                const unsigned char* text = sqlite3_column_text(stmt, i);
                row.emplace_back(text ? reinterpret_cast<const char*>(text) : "");
            }
            user = std::move(row);
        } else if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_finalize(stmt);
        return user;
    }

    // Deletes a user from the "users" table by username.
    void delete_user_by_username(const std::string& username) {
        const char* sql = "DELETE FROM users WHERE username = ?";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection_, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_finalize(stmt);
    }

    // Determines whether the user can log in, i.e. the user exists in the
    // database and the password is correct.
    bool validate_user_login(const std::string& username, const std::string& password) {
        auto user = search_user_by_username(username);
        if (user.has_value() && user->at(1) == password) {
            return true;
        }
        return false;
    }

private:
    sqlite3* connection_ = nullptr;
};