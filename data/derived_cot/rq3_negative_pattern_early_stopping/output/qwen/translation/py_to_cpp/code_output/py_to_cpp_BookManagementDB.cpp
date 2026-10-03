#include <sqlite3.h>
#include <string>
#include <vector>
#include <tuple>

class BookManagementDB {
private:
    sqlite3* db;
    sqlite3_stmt* stmt;

    int create_table() {
        const char* sql = "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, available INTEGER)";
        return sqlite3_exec(db, sql, nullptr, nullptr, nullptr);
    }

    int add_book(const std::string& title, const std::string& author) {
        const char* sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)";
        return execute_sql(sql, title, author);
    }

    int remove_book(int book_id) {
        const char* sql = "DELETE FROM books WHERE id = ?";
        return execute_sql(sql, book_id);
    }

    int borrow_book(int book_id) {
        const char* sql = "UPDATE books SET available = 0 WHERE id = ?";
        return execute_sql(sql, book_id);
    }

    int return_book(int book_id) {
        const char* sql = "UPDATE books SET available = 1 WHERE id = ?";
        return execute_sql(sql, book_id);
    }

    std::vector<std::tuple<int, std::string, std::string, int>> search_books() {
        std::vector<std::tuple<int, std::string, std::string, int>> books;
        const char* sql = "SELECT * FROM books";
        
        sqlite3_stmt* stmt;
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) return books;

        while (sqlite3_step(stmt) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const char* title = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            const char* author = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
            int available = sqlite3_column_int(stmt, 3);
            books.emplace_back(id, title, author, available);
        }

        sqlite3_finalize(stmt);
        return books;
    }

    int execute_sql(const char* sql, const std::string& param1, const std::string& param2 = "") {
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) return rc;

        if (sqlite3_bind_text(stmt, 1, param1.c_str(), -1, SQLITE_STATIC) != SQLITE_OK) {
            sqlite3_finalize(stmt);
            return -1;
        }

        if (!param2.empty() && sqlite3_bind_text(stmt, 2, param2.c_str(), -1, SQLITE_STATIC) != SQLITE_OK) {
            sqlite3_finalize(stmt);
            return -1;
        }

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            return -1;
        }

        sqlite3_finalize(stmt);
        return 0;
    }

public:
    BookManagementDB(const std::string& db_name) {
        int rc = sqlite3_open(db_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Cannot open database");
        }

        stmt = nullptr;
        create_table();
    }

    ~BookManagementDB() {
        if (stmt) sqlite3_finalize(stmt);
        if (db) sqlite3_close(db);
    }

    bool add_book(const std::string& title, const std::string& author) {
        return add_book(title, author) == 0;
    }

    bool remove_book(int book_id) {
        return remove_book(book_id) == 0;
    }

    bool borrow_book(int book_id) {
        return borrow_book(book_id) == 0;
    }

    bool return_book(int book_id) {
        return return_book(book_id) == 0;
    }

    std::vector<std::tuple<int, std::string, std::string, int>> search_books() {
        return search_books();
    }
};