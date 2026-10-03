#include <sqlite3.h>
#include <string>
#include <vector>
#include <tuple>

class BookManagementDB {
private:
    sqlite3* connection;

    sqlite3_stmt* prepareStatement(const std::string& sql) {
        sqlite3_stmt* stmt = nullptr;
        sqlite3_prepare_v2(connection, sql.c_str(), -1, &stmt, nullptr);
        return stmt;
    }

public:
    BookManagementDB(const std::string& db_name) {
        sqlite3_open(db_name.c_str(), &connection);
        create_table();
    }

    ~BookManagementDB() {
        sqlite3_close(connection);
    }

    // Disable copy to prevent double-close of the sqlite3 connection
    BookManagementDB(const BookManagementDB&) = delete;
    BookManagementDB& operator=(const BookManagementDB&) = delete;

    void create_table() {
        const char* sql =
            "CREATE TABLE IF NOT EXISTS books ("
            "id INTEGER PRIMARY KEY,"
            "title TEXT,"
            "author TEXT,"
            "available INTEGER"
            ")";
        sqlite3_exec(connection, sql, nullptr, nullptr, nullptr);
    }

    void add_book(const std::string& title, const std::string& author) {
        const char* sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)";
        sqlite3_stmt* stmt = prepareStatement(sql);
        sqlite3_bind_text(stmt, 1, title.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, author.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_step(stmt);
        sqlite3_finalize(stmt);
    }

    void remove_book(int book_id) {
        const char* sql = "DELETE FROM books WHERE id = ?";
        sqlite3_stmt* stmt = prepareStatement(sql);
        sqlite3_bind_int(stmt, 1, book_id);
        sqlite3_step(stmt);
        sqlite3_finalize(stmt);
    }

    void borrow_book(int book_id) {
        const char* sql = "UPDATE books SET available = 0 WHERE id = ?";
        sqlite3_stmt* stmt = prepareStatement(sql);
        sqlite3_bind_int(stmt, 1, book_id);
        sqlite3_step(stmt);
        sqlite3_finalize(stmt);
    }

    void return_book(int book_id) {
        const char* sql = "UPDATE books SET available = 1 WHERE id = ?";
        sqlite3_stmt* stmt = prepareStatement(sql);
        sqlite3_bind_int(stmt, 1, book_id);
        sqlite3_step(stmt);
        sqlite3_finalize(stmt);
    }

    std::vector<std::tuple<int, std::string, std::string, int>> search_books() {
        const char* sql = "SELECT * FROM books";
        sqlite3_stmt* stmt = prepareStatement(sql);
        std::vector<std::tuple<int, std::string, std::string, int>> books;
        while (sqlite3_step(stmt) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const char* title_ptr = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            const char* author_ptr = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
            std::string title = title_ptr ? title_ptr : "";
            std::string author = author_ptr ? author_ptr : "";
            int available = sqlite3_column_int(stmt, 3);
            books.emplace_back(id, title, author, available);
        }
        sqlite3_finalize(stmt);
        return books;
    }
};