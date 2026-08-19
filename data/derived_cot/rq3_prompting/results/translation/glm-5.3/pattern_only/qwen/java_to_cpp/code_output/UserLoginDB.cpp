#include <sqlite3.h>
#include <cstdio>
#include <optional>
#include <string>

class UserLoginDB {
private:
    sqlite3* connection;

    // Mirrors e.printStackTrace(): diagnostics to stderr, execution continues.
    void printSQLException(const char* context) {
        std::fprintf(stderr, "SQLException in %s: %s\n", context,
                     connection ? sqlite3_errmsg(connection) : "no connection available");
    }

    // Java: rs.getString(col) returns null for SQL NULL, and "str" + null -> "strnull"
    static std::string columnAsString(sqlite3_stmt* stmt, int col) {
        const unsigned char* text = sqlite3_column_text(stmt, col);
        return text ? std::string(reinterpret_cast<const char*>(text)) : std::string("null");
    }

public:
    explicit UserLoginDB(const std::string& dbName) : connection(nullptr) {
        if (sqlite3_open(dbName.c_str(), &connection) != SQLITE_OK) {
            printSQLException("DriverManager.getConnection");
            sqlite3_close(connection);
            connection = nullptr;
        } else {
            createTable();
        }
    }

    ~UserLoginDB() {
        close();
    }

    UserLoginDB(const UserLoginDB&) = delete;
    UserLoginDB& operator=(const UserLoginDB&) = delete;

private:
    void createTable() {
        const char* createTableQuery =
            "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)";
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, createTableQuery, -1, &pstmt, nullptr) != SQLITE_OK) {
            printSQLException("createTable: prepare");
            return;
        }
        if (sqlite3_step(pstmt) != SQLITE_DONE) {
            printSQLException("createTable: execute");
        }
        sqlite3_finalize(pstmt);
    }

public:
    void insertUser(const std::string& username, const std::string& password) {
        const char* insertQuery = "INSERT INTO users (username, password) VALUES (?, ?)";
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, insertQuery, -1, &pstmt, nullptr) != SQLITE_OK) {
            printSQLException("insertUser: prepare");
            return;
        }
        sqlite3_bind_text(pstmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(pstmt, 2, password.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(pstmt) != SQLITE_DONE) {
            printSQLException("insertUser: executeUpdate");
        }
        sqlite3_finalize(pstmt);
    }

    // Java returns null on miss/error; std::optional preserves that contract.
    std::optional<std::string> searchUserByUsername(const std::string& username) {
        const char* searchQuery = "SELECT * FROM users WHERE username = ?";
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, searchQuery, -1, &pstmt, nullptr) != SQLITE_OK) {
            printSQLException("searchUserByUsername: prepare");
            return std::nullopt;
        }
        sqlite3_bind_text(pstmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);

        std::optional<std::string> result;
        if (sqlite3_step(pstmt) == SQLITE_ROW) {
            // getString("username") / getString("password") -> columns 0 and 1 of users
            result = columnAsString(pstmt, 0) + "," + columnAsString(pstmt, 1);
        }
        sqlite3_finalize(pstmt);
        return result;
    }

    void deleteUserByUsername(const std::string& username) {
        const char* deleteQuery = "DELETE FROM users WHERE username = ?";
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, deleteQuery, -1, &pstmt, nullptr) != SQLITE_OK) {
            printSQLException("deleteUserByUsername: prepare");
            return;
        }
        sqlite3_bind_text(pstmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(pstmt) != SQLITE_DONE) {
            printSQLException("deleteUserByUsername: executeUpdate");
        }
        sqlite3_finalize(pstmt);
    }

    bool validateUserLogin(const std::string& username, const std::string& password) {
        std::optional<std::string> user = searchUserByUsername(username);
        if (user.has_value()) {
            const std::string& s = *user;
            // Java: parts = user.split(","); return parts[1].equals(password);
            // parts[1] is the segment between the first and second ',' (or end).
            std::size_t first = s.find(',');
            if (first == std::string::npos) {
                // Unreachable given the constructed format; mirrors IndexOutOfBounds failure.
                return false;
            }
            std::size_t second = s.find(',', first + 1);
            std::size_t end = (second == std::string::npos) ? s.size() : second;
            std::string stored = s.substr(first + 1, end - (first + 1));
            return stored == password;
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