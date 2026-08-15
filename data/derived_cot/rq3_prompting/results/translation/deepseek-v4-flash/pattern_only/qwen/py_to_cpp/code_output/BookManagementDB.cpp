#include <sqlite3.h>
#include <string>
#include <vector>
#include <tuple>
#include <stdexcept>

class BookManagementDB {
public:
    BookManagementDB(const std::string& db_name) : connection(nullptr) {
        int rc = sqlite3_open(db_name.c_str(), &connection);
        if (rc != SQLITE_OK) {
            std::string msg = connection ? sqlite3_errmsg(connection) : "Failed to open database";
            if (connection) sqlite3_close(connection);
            throw std::runtime_error(msg);
        }
        try {
            create_table();
        } catch (...) {
            sqlite3_close(connection);
            connection = nullptr;
            throw;
        }
    }

    ~BookManagementDB() {
        if (connection) {
            sqlite3_close(connection);
        }
    }

    void create_table() {
        const char* sql = "CREATE TABLE IF NOT EXISTS books ("
                          "id INTEGER PRIMARY KEY, "
                          "title TEXT, "
                          "author TEXT, "
                          "available INTEGER)";
        char* errMsg = nullptr;
        int rc = sqlite3_exec(connection, sql, nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::string msg = errMsg ? errMsg : "SQL error";
            sqlite3_free(errMsg);
            throw std::runtime_error(msg);
        }
    }

    void add_book(const std::string& title, const std::string& author) {
        const char* sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection));
        }
        int rc1 = sqlite3_bind_text(stmt, 1, title.c_str(), -1, SQLITE_TRANSIENT);
        int rc2 = sqlite3_bind_text(stmt, 2, author.c_str(), -1, SQLITE_TRANSIENT);
        if (rc1 != SQLITE_OK || rc2 != SQLITE_OK) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error(msg);
        }
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error(msg);
        }
        sqlite3_finalize(stmt);
    }

    void remove_book(int book_id) {
        const char* sql = "DELETE FROM books WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection));
        }
        if (sqlite3_bind_int(stmt, 1, book_id) != SQLITE_OK) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error(msg);
        }
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error(msg);
        }
        sqlite3_finalize(stmt);
    }

    void borrow_book(int book_id) {
        const char* sql = "UPDATE books SET available = 0 WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection));
        }
        if (sqlite3_bind_int(stmt, 1, book_id) != SQLITE_OK) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error(msg);
        }
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error(msg);
        }
        sqlite3_finalize(stmt);
    }

    void return_book(int book_id) {
        const char* sql = "UPDATE books SET available = 1 WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection));
        }
        if (sqlite3_bind_int(stmt, 1, book_id) != SQLITE_OK) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error(msg);
        }
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error(msg);
        }
        sqlite3_finalize(stmt);
    }

    std::vector<std::tuple<int, std::string, std::string, int>> search_books() {
        const char* sql = "SELECT * FROM books";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection));
        }

        std::vector<std::tuple<int, std::string, std::string, int>> books;
        int rc;
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const unsigned char* title_text = sqlite3_column_text(stmt, 1);
            const unsigned char* author_text = sqlite3_column_text(stmt, 2);
            int available = sqlite3_column_int(stmt, 3);

            std::string title = title_text ? reinterpret_cast<const char*>(title_text) : "";
            std::string author = author_text ? reinterpret_cast<const char*>(author_text) : "";
            books.emplace_back(id, title, author, available);
        }

        if (rc != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error(msg);
        }

        sqlite3_finalize(stmt);
        return books;
    }

private:
    sqlite3* connection;
};