#include <sqlite3.h>
#include <optional>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class UserLoginDB {
public:
    explicit UserLoginDB(const std::string& db_name) {
        if (sqlite3_open(db_name.c_str(), &connection_) != SQLITE_OK) {
            const std::string msg = connection_ ? sqlite3_errmsg(connection_)
                                                : "unable to open database file";
            if (connection_) {
                sqlite3_close(connection_);
            }
            connection_ = nullptr;
            throw std::runtime_error(msg);
        }
    }

    ~UserLoginDB() {
        if (connection_ != nullptr) {
            sqlite3_close(connection_);
        }
    }

    // The Python connection object has no meaningful copy semantics.
    UserLoginDB(const UserLoginDB&) = delete;
    UserLoginDB& operator=(const UserLoginDB&) = delete;

    void insert_user(const std::string& username, const std::string& password) {
        execute("INSERT INTO users (username, password) VALUES (?, ?)",
                {username, password});
        commit();
    }

    // Equivalent of fetchone(): one row (as column values) or no value.
    std::optional<std::vector<std::string>> search_user_by_username(
        const std::string& username) {
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection_,
                               "SELECT * FROM users WHERE username = ?",
                               -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);

        std::optional<std::vector<std::string>> result;
        const int rc = sqlite3_step(stmt);
        if (rc == SQLITE_ROW) {
            std::vector<std::string> row;
            const int cols = sqlite3_column_count(stmt);
            row.reserve(static_cast<size_t>(cols));
            for (int i = 0; i < cols; ++i) {
                const unsigned char* text = sqlite3_column_text(stmt, i);
                row.emplace_back(text != nullptr
                                     ? reinterpret_cast<const char*>(text)
                                     : std::string());
            }
            result = std::move(row);
        } else if (rc != SQLITE_DONE) {
            const std::string msg = sqlite3_errmsg(connection_);
            sqlite3_finalize(stmt);
            throw std::runtime_error(msg);
        }
        sqlite3_finalize(stmt);
        return result;
    }

    void delete_user_by_username(const std::string& username) {
        execute("DELETE FROM users WHERE username = ?", {username});
        commit();
    }

    bool validate_user_login(const std::string& username,
                             const std::string& password) {
        const auto user = search_user_by_username(username);
        return user.has_value() && (*user)[1] == password;
    }

private:
    void execute(const char* sql, const std::vector<std::string>& params) {
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection_, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        for (size_t i = 0; i < params.size(); ++i) {
            sqlite3_bind_text(stmt, static_cast<int>(i + 1),
                              params[i].c_str(), -1, SQLITE_TRANSIENT);
        }
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            const std::string msg = sqlite3_errmsg(connection_);
            sqlite3_finalize(stmt);
            throw std::runtime_error(msg);
        }
        sqlite3_finalize(stmt);
    }

    void commit() {
        char* err = nullptr;
        if (sqlite3_exec(connection_, "COMMIT", nullptr, nullptr, &err) != SQLITE_OK) {
            const std::string msg = err != nullptr ? err : "commit failed";
            sqlite3_free(err);
            throw std::runtime_error(msg);
        }
    }

    sqlite3* connection_ = nullptr;
};