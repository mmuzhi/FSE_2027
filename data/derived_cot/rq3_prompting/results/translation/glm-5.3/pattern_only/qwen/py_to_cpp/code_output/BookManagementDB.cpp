#include <sqlite3.h>
#include <string>
#include <vector>
#include <tuple>
#include <stdexcept>

class BookManagementDB {
public:
    explicit BookManagementDB(const std::string& db_name) {
        if (sqlite3_open(db_name.c_str(), &connection) != SQLITE_OK) {
            std::string err = connection ? sqlite3_errmsg(connection)
                                         : "unable to open database file";
            sqlite3_close(connection);
            connection = nullptr;
            throw std::runtime_error(err);
        }
        create_table();
    }

    ~BookManagementDB() {
        if (connection) {
            sqlite3_close(connection);
            connection = nullptr;
        }
    }

    BookManagementDB(const BookManagementDB&) = delete;
    BookManagementDB& operator=(const BookManagementDB&) = delete;

    void create_table() {
        const char* sql =
            "CREATE TABLE IF NOT EXISTS books ("
            "id INTEGER PRIMARY KEY, "
            "title TEXT, "
            "author TEXT, "
            "available INTEGER"
            ");";
        char* err = nullptr;
        if (sqlite3_exec(connection, sql, nullptr, nullptr, &err) != SQLITE_OK) {
            std::string msg = err ? err : "unknown error";
            sqlite3_free(err);
            throw std::runtime_error(msg);
        }
    }

    void add_book(const std::string& title, const std::string& author) {
        const char* sql =
            "INSERT INTO books (title, author, available) VALUES (?, ?, 1);";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection));
        }
        sqlite3_bind_text(stmt, 1, title.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, author.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error(msg);
        }
        sqlite3_finalize(stmt);
    }

    void remove_book(int book_id) {
        execute("DELETE FROM books WHERE id = ?;", book_id);
    }

    void borrow_book(int book_id) {
        execute("UPDATE books SET available = 0 WHERE id = ?;", book_id);
    }

    void return_book(int book_id) {
        execute("UPDATE books SET available = 1 WHERE id = ?;", book_id);
    }

    std::vector<std::tuple<int, std::string, std::string, int>> search_books() {
        const char* sql = "SELECT * FROM books;";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection));
        }
        std::vector<std::tuple<int, std::string, std::string, int>> books;
        while (sqlite3_step(stmt) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const unsigned char* title = sqlite3_column_text(stmt, 1);
            const unsigned char* author = sqlite3_column_text(stmt, 2);
            int available = sqlite3_column_int(stmt, 3);
            books.emplace_back(
                id,
                title ? reinterpret_cast<const char*>(title) : "",
                author ? reinterpret_cast<const char*>(author) : "",
                available);
        }
        sqlite3_finalize(stmt);
        return books;
    }

private:
    sqlite3* connection = nullptr;

    void execute(const char* sql, int book_id) {
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection));
        }
        sqlite3_bind_int(stmt, 1, book_id);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error(msg);
        }
        sqlite3_finalize(stmt);
    }
};