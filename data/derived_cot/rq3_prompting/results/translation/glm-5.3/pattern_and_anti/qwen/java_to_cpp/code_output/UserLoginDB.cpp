#include <cstdio>
#include <optional>
#include <string>
#include <sqlite3.h>

class UserLoginDB {
private:
    sqlite3* connection = nullptr;

    // Emulates java.sql.SQLException.printStackTrace() (stderr output)
    static void printStackTrace(const std::string& message) {
        std::fprintf(stderr, "java.sql.SQLException: %s\n", message.c_str());
    }

    bool ensureConnection() {
        if (connection == nullptr) {
            printStackTrace("database connection is not open");
            return false;
        }
        return true;
    }

    // Java ResultSet.getString() returns null for NULL columns; string
    // concatenation renders null as "null".
    static std::string columnText(sqlite3_stmt* stmt, int col) {
        const unsigned char* text = sqlite3_column_text(stmt, col);
        return text != nullptr
            ? std::string(reinterpret_cast<const char*>(text))
            : std::string("null");
    }

    void createTable() {
        if (!ensureConnection()) return;
        const char* createTableQuery =
            "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)";
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, createTableQuery, -1, &pstmt, nullptr) != SQLITE_OK) {
            printStackTrace(sqlite3_errmsg(connection));
            return;
        }
        if (sqlite3_step(pstmt) != SQLITE_DONE) {
            printStackTrace(sqlite3_errmsg(connection));
        }
        sqlite3_finalize(pstmt); // try-with-resources: statement always released
    }

public:
    explicit UserLoginDB(const std::string& dbName) {
        if (sqlite3_open(dbName.c_str(), &connection) != SQLITE_OK) {
            printStackTrace(connection != nullptr ? sqlite3_errmsg(connection)
                                                  : "unable to open database");
            sqlite3_close(connection);
            connection = nullptr; // like Java: connection stays null on failure
        } else {
            createTable();
        }
    }

    ~UserLoginDB() {
        close();
    }

    UserLoginDB(const UserLoginDB&) = delete;
    UserLoginDB& operator=(const UserLoginDB&) = delete;

    void insertUser(const std::string& username, const std::string& password) {
        if (!ensureConnection()) return;
        const char* insertQuery =
            "INSERT INTO users (username, password) VALUES (?, ?)";
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, insertQuery, -1, &pstmt, nullptr) != SQLITE_OK) {
            printStackTrace(sqlite3_errmsg(connection));
            return;
        }
        sqlite3_bind_text(pstmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(pstmt, 2, password.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(pstmt) != SQLITE_DONE) {
            printStackTrace(sqlite3_errmsg(connection));
        }
        sqlite3_finalize(pstmt);
    }

    // Returns std::nullopt where the Java version returns null
    std::optional<std::string> searchUserByUsername(const std::string& username) {
        if (!ensureConnection()) return std::nullopt;
        const char* searchQuery = "SELECT * FROM users WHERE username = ?";
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, searchQuery, -1, &pstmt, nullptr) != SQLITE_OK) {
            printStackTrace(sqlite3_errmsg(connection));
            return std::nullopt;
        }
        std::optional<std::string> result;
        sqlite3_bind_text(pstmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(pstmt) == SQLITE_ROW) {
            result = columnText(pstmt, 0) + "," + columnText(pstmt, 1);
        }
        sqlite3_finalize(pstmt);
        return result;
    }

    void deleteUserByUsername(const std::string& username) {
        if (!ensureConnection()) return;
        const char* deleteQuery = "DELETE FROM users WHERE username = ?";
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, deleteQuery, -1, &pstmt, nullptr) != SQLITE_OK) {
            printStackTrace(sqlite3_errmsg(connection));
            return;
        }
        sqlite3_bind_text(pstmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(pstmt) != SQLITE_DONE) {
            printStackTrace(sqlite3_errmsg(connection));
        }
        sqlite3_finalize(pstmt);
    }

    bool validateUserLogin(const std::string& username, const std::string& password) {
        std::optional<std::string> user = searchUserByUsername(username);
        if (user.has_value()) {
            const std::string& u = *user;
            // Mirrors Java user.split(",")[1]: segment between the first
            // and second comma (not the whole remainder).
            std::size_t first = u.find(',');
            std::size_t second = u.find(',', first + 1);
            std::size_t len =
                (second == std::string::npos ? u.size() : second) - (first + 1);
            return u.substr(first + 1, len) == password;
        }
        return false;
    }

    void close() {
        if (connection != nullptr) {
            sqlite3_close(connection);
            connection = nullptr;
        }
    }
};