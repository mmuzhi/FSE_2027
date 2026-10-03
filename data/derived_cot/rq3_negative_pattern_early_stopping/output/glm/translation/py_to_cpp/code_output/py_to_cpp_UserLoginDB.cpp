#include <string>
#include <vector>
#include <optional>
#include <sqlite3.h>

class UserLoginDB {
private:
    sqlite3* connection;

public:
    UserLoginDB(const std::string& db_name) {
        sqlite3_open(db_name.c_str(), &connection);
    }

    ~UserLoginDB() {
        if (connection) {
            sqlite3_close(connection);
        }
    }

    void insert_user(const std::string& username, const std::string& password) {
        sqlite3_stmt* stmt;
        const char* sql = "INSERT INTO users (username, password) VALUES (?, ?);";
        sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, password.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_step(stmt);
        sqlite3_finalize(stmt);
        sqlite3_exec(connection, "COMMIT;", nullptr, nullptr, nullptr);
    }

    std::optional<std::vector<std::string>> search_user_by_username(const std::string& username) {
        sqlite3_stmt* stmt;
        const char* sql = "SELECT * FROM users WHERE username = ?;";
        sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        
        std::optional<std::vector<std::string>> result;
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            std::vector<std::string> row;
            int cols = sqlite3_column_count(stmt);
            for (int i = 0; i < cols; ++i) {
                const char* text = reinterpret_cast<const char*>(sqlite3_column_text(stmt, i));
                if (text) {
                    row.push_back(text);
                } else {
                    row.push_back("");
                }
            }
            result = row;
        }
        sqlite3_finalize(stmt);
        return result;
    }

    void delete_user_by_username(const std::string& username) {
        sqlite3_stmt* stmt;
        const char* sql = "DELETE FROM users WHERE username = ?;";
        sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_step(stmt);
        sqlite3_finalize(stmt);
        sqlite3_exec(connection, "COMMIT;", nullptr, nullptr, nullptr);
    }

    bool validate_user_login(const std::string& username, const std::string& password) {
        auto user = search_user_by_username(username);
        if (user.has_value() && (*user)[1] == password) {
            return true;
        }
        return false;
    }
};