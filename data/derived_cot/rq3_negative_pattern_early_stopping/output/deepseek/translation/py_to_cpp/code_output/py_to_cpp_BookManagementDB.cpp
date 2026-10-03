#include <sqlite3.h>
#include <string>
#include <vector>
#include <tuple>
#include <stdexcept>

class BookManagementDB {
private:
    sqlite3* db;

    void execute_sql(const std::string& sql) {
        char* errMsg = nullptr;
        int rc = sqlite3_exec(db, sql.c_str(), nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::string error = errMsg ? errMsg : "Unknown error";
            sqlite3_free(errMsg);
            throw std::runtime_error("SQL error: " + error);
        }
    }

public:
    BookManagementDB(const std::string& db_name) {
        int rc = sqlite3_open(db_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Cannot open database: " + std::string(sqlite3_errmsg(db)));
        }
        create_table();
    }

    ~BookManagementDB() {
        if (db) {
            sqlite3_close(db);
        }
    }

    void create_table() {
        const char* sql = "CREATE TABLE IF NOT EXISTS books ("
                          "id INTEGER PRIMARY KEY,"
                          "title TEXT,"
                          "author TEXT,"
                          "available INTEGER"
                          ")";
        execute_sql(sql);
    }

    void add_book(const std::string& title, const std::string& author) {
        sqlite3_stmt* stmt;
        const char* sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)";
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare statement: " + std::string(sqlite3_errmsg(db)));
        }
        sqlite3_bind_text(stmt, 1, title.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, author.c_str(), -1, SQLITE_TRANSIENT);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to insert book: " + std::string(sqlite3_errmsg(db)));
        }
        sqlite3_finalize(stmt);
    }

    void remove_book(int book_id) {
        sqlite3_stmt* stmt;
        const char* sql = "DELETE FROM books WHERE id = ?";
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare statement: " + std::string(sqlite3_errmsg(db)));
        }
        sqlite3_bind_int(stmt, 1, book_id);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to delete book: " + std::string(sqlite3_errmsg(db)));
        }
        sqlite3_finalize(stmt);
    }

    void borrow_book(int book_id) {
        sqlite3_stmt* stmt;
        const char* sql = "UPDATE books SET available = 0 WHERE id = ?";
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare statement: " + std::string(sqlite3_errmsg(db)));
        }
        sqlite3_bind_int(stmt, 1, book_id);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to borrow book: " + std::string(sqlite3_errmsg(db)));
        }
        sqlite3_finalize(stmt);
    }

    void return_book(int book_id) {
        sqlite3_stmt* stmt;
        const char* sql = "UPDATE books SET available = 1 WHERE id = ?";
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare statement: " + std::string(sqlite3_errmsg(db)));
        }
        sqlite3_bind_int(stmt, 1, book_id);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to return book: " + std::string(sqlite3_errmsg(db)));
        }
        sqlite3_finalize(stmt);
    }

    std::vector<std::tuple<int, std::string, std::string, int>> search_books() {
        std::vector<std::tuple<int, std::string, std::string, int>> books;
        sqlite3_stmt* stmt;
        const char* sql = "SELECT * FROM books";
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare statement: " + std::string(sqlite3_errmsg(db)));
        }
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const unsigned char* title = sqlite3_column_text(stmt, 1);
            const unsigned char* author = sqlite3_column_text(stmt, 2);
            int available = sqlite3_column_int(stmt, 3);
            books.emplace_back(id,
                               std::string(reinterpret_cast<const char*>(title)),
                               std::string(reinterpret_cast<const char*>(author)),
                               available);
        }
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to fetch books: " + std::string(sqlite3_errmsg(db)));
        }
        sqlite3_finalize(stmt);
        return books;
    }
};