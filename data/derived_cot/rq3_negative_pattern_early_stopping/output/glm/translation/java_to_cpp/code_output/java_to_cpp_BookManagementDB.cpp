#include <sqlite3.h>
#include <string>
#include <vector>
#include <stdexcept>
#include <utility>

class BookManagementDB {
public:
    class Book {
    private:
        int id_;
        std::string title_;
        std::string author_;
        int available_;

    public:
        Book(int id, std::string title, std::string author, int available)
            : id_(id), title_(std::move(title)), author_(std::move(author)), available_(available) {}

        int getId() const { return id_; }
        const std::string& getTitle() const { return title_; }
        const std::string& getAuthor() const { return author_; }
        int getAvailable() const { return available_; }

        std::string toString() const {
            return "Book{id=" + std::to_string(id_) +
                   ", title='" + title_ + '\'' +
                   ", author='" + author_ + '\'' +
                   ", available=" + std::to_string(available_) +
                   '}';
        }
    };

private:
    sqlite3* connection_;

    void throwError(const std::string& prefix) {
        throw std::runtime_error(prefix + ": " + std::string(sqlite3_errmsg(connection_)));
    }

    struct StmtGuard {
        sqlite3_stmt* stmt;
        explicit StmtGuard(sqlite3_stmt* s) : stmt(s) {}
        ~StmtGuard() { if (stmt) sqlite3_finalize(stmt); }
        StmtGuard(const StmtGuard&) = delete;
        StmtGuard& operator=(const StmtGuard&) = delete;
    };

public:
    BookManagementDB(const std::string& dbName) : connection_(nullptr) {
        int rc = sqlite3_open(dbName.c_str(), &connection_);
        if (rc != SQLITE_OK) {
            std::string errMsg = connection_ ? sqlite3_errmsg(connection_) : "unknown error";
            if (connection_) sqlite3_close(connection_);
            connection_ = nullptr;
            throw std::runtime_error("Failed to open database: " + errMsg);
        }
        createTable();
    }

    ~BookManagementDB() {
        if (connection_) {
            sqlite3_close(connection_);
            connection_ = nullptr;
        }
    }

    BookManagementDB(const BookManagementDB&) = delete;
    BookManagementDB& operator=(const BookManagementDB&) = delete;

    void createTable() {
        const char* sql =
            "CREATE TABLE IF NOT EXISTS books ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT, "
            "author TEXT, "
            "available INTEGER"
            ")";
        char* errMsg = nullptr;
        int rc = sqlite3_exec(connection_, sql, nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::string err = errMsg ? errMsg : "unknown error";
            sqlite3_free(errMsg);
            throw std::runtime_error("createTable: " + err);
        }
    }

    void addBook(const std::string& title, const std::string& author) {
        const char* sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)";
        sqlite3_stmt* pstmt = nullptr;
        int rc = sqlite3_prepare_v2(connection_, sql, -1, &pstmt, nullptr);
        if (rc != SQLITE_OK) throwError("addBook prepare");
        StmtGuard guard(pstmt);

        rc = sqlite3_bind_text(pstmt, 1, title.c_str(), static_cast<int>(title.size()), SQLITE_TRANSIENT);
        if (rc != SQLITE_OK) throwError("addBook bind title");

        rc = sqlite3_bind_text(pstmt, 2, author.c_str(), static_cast<int>(author.size()), SQLITE_TRANSIENT);
        if (rc != SQLITE_OK) throwError("addBook bind author");

        rc = sqlite3_step(pstmt);
        if (rc != SQLITE_DONE) throwError("addBook step");
    }

    void removeBook(int bookId) {
        const char* sql = "DELETE FROM books WHERE id = ?";
        sqlite3_stmt* pstmt = nullptr;
        int rc = sqlite3_prepare_v2(connection_, sql, -1, &pstmt, nullptr);
        if (rc != SQLITE_OK) throwError("removeBook prepare");
        StmtGuard guard(pstmt);

        rc = sqlite3_bind_int(pstmt, 1, bookId);
        if (rc != SQLITE_OK) throwError("removeBook bind");

        rc = sqlite3_step(pstmt);
        if (rc != SQLITE_DONE) throwError("removeBook step");
    }

    void borrowBook(int bookId) {
        const char* sql = "UPDATE books SET available = 0 WHERE id = ?";
        sqlite3_stmt* pstmt = nullptr;
        int rc = sqlite3_prepare_v2(connection_, sql, -1, &pstmt, nullptr);
        if (rc != SQLITE_OK) throwError("borrowBook prepare");
        StmtGuard guard(pstmt);

        rc = sqlite3_bind_int(pstmt, 1, bookId);
        if (rc != SQLITE_OK) throwError("borrowBook bind");

        rc = sqlite3_step(pstmt);
        if (rc != SQLITE_DONE) throwError("borrowBook step");
    }

    void returnBook(int bookId) {
        const char* sql = "UPDATE books SET available = 1 WHERE id = ?";
        sqlite3_stmt* pstmt = nullptr;
        int rc = sqlite3_prepare_v2(connection_, sql, -1, &pstmt, nullptr);
        if (rc != SQLITE_OK) throwError("returnBook prepare");
        StmtGuard guard(pstmt);

        rc = sqlite3_bind_int(pstmt, 1, bookId);
        if (rc != SQLITE_OK) throwError("returnBook bind");

        rc = sqlite3_step(pstmt);
        if (rc != SQLITE_DONE) throwError("returnBook step");
    }

    std::vector<Book> searchBooks() {
        const char* sql = "SELECT * FROM books";
        std::vector<Book> books;
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection_, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) throwError("searchBooks prepare");
        StmtGuard guard(stmt);

        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const unsigned char* titlePtr = sqlite3_column_text(stmt, 1);
            std::string title = titlePtr ? reinterpret_cast<const char*>(titlePtr) : "";
            const unsigned char* authorPtr = sqlite3_column_text(stmt, 2);
            std::string author = authorPtr ? reinterpret_cast<const char*>(authorPtr) : "";
            int available = sqlite3_column_int(stmt, 3);
            books.emplace_back(id, title, author, available);
        }

        if (rc != SQLITE_DONE) throwError("searchBooks step");

        return books;
    }
};