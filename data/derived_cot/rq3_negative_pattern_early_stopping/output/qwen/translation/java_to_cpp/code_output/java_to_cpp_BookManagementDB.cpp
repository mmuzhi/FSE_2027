#include <sqlite3.h>
#include <string>
#include <vector>
#include <stdexcept>
#include <memory>

struct Book {
    int id;
    std::string title;
    std::string author;
    int available;

    Book(int id, const std::string& title, const std::string& author, int available)
        : id(id), title(title), author(author), available(available) {}
};

class BookManagementDB {
private:
    sqlite3* db;
    struct Exception : std::runtime_error {
        explicit Exception(const std::string& msg) : runtime_error(msg) {}
    };

    void check_sqlite_error(const char* op) const {
        if (sqlite3_errcode(db) != SQLITE_OK) {
            throw Exception(sqlite3_errmsg(db));
        }
    }

public:
    explicit BookManagementDB(const std::string& dbName)
        : db(nullptr) {
        int rc = sqlite3_open(dbName.c_str(), &db);
        if (rc != SQLITE_OK) {
            throw Exception("Failed to open database");
        }
        createTable();
    }

    ~BookManagementDB() {
        if (db) {
            sqlite3_close(db);
        }
    }

    void createTable() {
        const char* sql = "CREATE TABLE IF NOT EXISTS books ("
                          "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                          "title TEXT, "
                          "author TEXT, "
                          "available INTEGER)";
        char* errorMsg = nullptr;
        int rc = sqlite3_exec(db, sql, nullptr, nullptr, &errorMsg);
        if (rc != SQLITE_OK) {
            if (errorMsg) {
                throw Exception(errorMsg);
                sqlite3_free(errorMsg);
            }
        }
    }

    void addBook(const std::string& title, const std::string& author) {
        std::string sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw Exception("Failed to prepare statement");
        }

        sqlite3_bind_text(stmt, 1, title.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 2, author.c_str(), -1, SQLITE_STATIC);
        check_sqlite_error("bind parameters");

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            throw Exception("Failed to insert book");
        }
        sqlite3_finalize(stmt);
    }

    void removeBook(int bookId) {
        std::string sql = "DELETE FROM books WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw Exception("Failed to prepare statement");
        }

        sqlite3_bind_int(stmt, 1, bookId);
        check_sqlite_error("bind parameter");

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            throw Exception("Failed to delete book");
        }
        sqlite3_finalize(stmt);
    }

    void borrowBook(int bookId) {
        std::string sql = "UPDATE books SET available = 0 WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw Exception("Failed to prepare statement");
        }

        sqlite3_bind_int(stmt, 1, bookId);
        check_sqlite_error("bind parameter");

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            throw Exception("Failed to borrow book");
        }
        sqlite3_finalize(stmt);
    }

    void returnBook(int bookId) {
        std::string sql = "UPDATE books SET available = 1 WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw Exception("Failed to prepare statement");
        }

        sqlite3_bind_int(stmt, 1, bookId);
        check_sqlite_error("bind parameter");

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            throw Exception("Failed to return book");
        }
        sqlite3_finalize(stmt);
    }

    std::vector<Book> searchBooks() {
        std::string sql = "SELECT * FROM books";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw Exception("Failed to prepare statement");
        }

        std::vector<Book> books;
        while (SQLITE_ROW == sqlite3_step(stmt)) {
            int id = sqlite3_column_int(stmt, 0);
            const char* title = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            const char* author = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
            int available = sqlite3_column_int(stmt, 3);
            books.emplace_back(id, title != nullptr ? std::string(title) : "", 
                              author != nullptr ? std::string(author) : "", available);
        }
        sqlite3_finalize(stmt);
        return books;
    }
};