#include <sqlite3.h>
#include <string>
#include <vector>
#include <stdexcept>
#include <sstream>
#include <memory>

class BookManagementDB {
public:
    struct Book {
    private:
        int id_;
        std::string title_;
        std::string author_;
        int available_;
    public:
        Book(int id, const std::string& title, const std::string& author, int available)
            : id_(id), title_(title), author_(author), available_(available) {}

        int getId() const { return id_; }
        const std::string& getTitle() const { return title_; }
        const std::string& getAuthor() const { return author_; }
        int getAvailable() const { return available_; }

        std::string toString() const {
            std::ostringstream oss;
            oss << "Book{id=" << id_
                << ", title='" << title_ << '\''
                << ", author='" << author_ << '\''
                << ", available=" << available_ << '}';
            return oss.str();
        }
    };

    explicit BookManagementDB(const std::string& dbName) {
        int rc = sqlite3_open(dbName.c_str(), &db_);
        if (rc != SQLITE_OK) {
            std::string err = "Failed to open database: " + std::string(sqlite3_errmsg(db_));
            if (db_) sqlite3_close(db_);
            throw std::runtime_error(err);
        }
        createTable();
    }

    ~BookManagementDB() {
        if (db_) sqlite3_close(db_);
    }

    void addBook(const std::string& title, const std::string& author) {
        const char* sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare statement: " + std::string(sqlite3_errmsg(db_)));
        }
        // Bind values
        sqlite3_bind_text(stmt, 1, title.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, author.c_str(), -1, SQLITE_TRANSIENT);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to execute insert: " + std::string(sqlite3_errmsg(db_)));
        }
        sqlite3_finalize(stmt);
    }

    void removeBook(int bookId) {
        const char* sql = "DELETE FROM books WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare delete: " + std::string(sqlite3_errmsg(db_)));
        }
        sqlite3_bind_int(stmt, 1, bookId);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to execute delete: " + std::string(sqlite3_errmsg(db_)));
        }
        sqlite3_finalize(stmt);
    }

    void borrowBook(int bookId) {
        const char* sql = "UPDATE books SET available = 0 WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare borrow: " + std::string(sqlite3_errmsg(db_)));
        }
        sqlite3_bind_int(stmt, 1, bookId);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to execute borrow: " + std::string(sqlite3_errmsg(db_)));
        }
        sqlite3_finalize(stmt);
    }

    void returnBook(int bookId) {
        const char* sql = "UPDATE books SET available = 1 WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare return: " + std::string(sqlite3_errmsg(db_)));
        }
        sqlite3_bind_int(stmt, 1, bookId);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to execute return: " + std::string(sqlite3_errmsg(db_)));
        }
        sqlite3_finalize(stmt);
    }

    std::vector<Book> searchBooks() {
        const char* sql = "SELECT * FROM books";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare select: " + std::string(sqlite3_errmsg(db_)));
        }

        std::vector<Book> books;
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const char* title = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            const char* author = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
            int available = sqlite3_column_int(stmt, 3);
            books.emplace_back(id,
                               title ? title : "",
                               author ? author : "",
                               available);
        }
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Error iterating results: " + std::string(sqlite3_errmsg(db_)));
        }
        sqlite3_finalize(stmt);
        return books;
    }

private:
    sqlite3* db_ = nullptr;

    void createTable() {
        const char* sql = "CREATE TABLE IF NOT EXISTS books ("
                          "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                          "title TEXT, "
                          "author TEXT, "
                          "available INTEGER"
                          ")";
        char* errMsg = nullptr;
        int rc = sqlite3_exec(db_, sql, nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::string err = "Failed to create table: " + std::string(errMsg);
            sqlite3_free(errMsg);
            throw std::runtime_error(err);
        }
    }
};