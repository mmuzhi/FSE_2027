#include <sqlite3.h>
#include <stdexcept>
#include <vector>
#include <tuple>
#include <string>

class UserLoginDB {
private:
    sqlite3* db;

public:
    UserLoginDB(const std::string& db_name) {
        int rc = sqlite3_open(db_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db));
        }
    }

    ~UserLoginDB() {
        if (db) {
            sqlite3_close(db);
        }
    }

    void insert_user(const std::string& username, const std::string& password) {
        const char* sql = "INSERT INTO users (username, password) VALUES (?, ?)";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db));
        }

        sqlite3_bind_text(stmt, 1, username.c_str(), username.size(), SQLITE_STATIC);
        sqlite3_bind_text(stmt, 2, password.c_str(), password.size(), SQLITE_STATIC);

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error(sqlite3_errmsg(db));
        }

        sqlite3_finalize(stmt);
    }

    std::vector<std::tuple<std::string, std::string>> search_user_by_username(const std::string& username) {
        const char* sql = "SELECT * FROM users WHERE username = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db));
        }

        sqlite3_bind_text(stmt, 1, username.c_str(), username.size(), SQLITE_STATIC);

        std::vector<std::tuple<std::string, std::string>> result;
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            const unsigned char* name = sqlite3_column_text(stmt, 0);
            const unsigned char* pass = sqlite3_column_text(stmt, 1);
            if (name && pass) {
                result.push_back(std::make_tuple(std::string((const char*)name), std::string((const char*)pass)));
            }
        }

        sqlite3_finalize(stmt);
        return result;
    }

    void delete_user_by_username(const std::string& username) {
        const char* sql = "DELETE FROM users WHERE username = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db));
        }

        sqlite3_bind_text(stmt, 1, username.c_str(), username.size(), SQLITE_STATIC);

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error(sqlite3_errmsg(db));
        }

        sqlite3_finalize(stmt);
    }

    bool validate_user_login(const std::string& username, const std::string& password) {
        auto user = search_user_by_username(username);
        if (user.empty()) {
            return false;
        }
        return std::get<1>(user[0]) == password;
    }
};