#include <sqlite3.h>
#include <stdexcept>
#include <string>
#include <vector>

class BookManagementDB {
public:
    class Book {
    private:
        int id;
        std::string title;
        std::string author;
        int available;

    public:
        Book(int id, const std::string& title, const std::string& author, int available)
            : id(id), title(title), author(author), available(available) {}

        int getId() const { return id; }
        const std::string& getTitle() const { return title; }
        const std::string& getAuthor() const { return author; }
        int getAvailable() const { return available; }

        std::string toString() const {
            return "Book{id=" + std::to_string(id) +
                   ", title='" + title + "'" +
                   ", author='" + author + "'" +
                   ", available=" + std::to_string(available) +
                   "}";
        }
    };

    explicit BookManagementDB(const std::string& dbName) {
        // Equivalent of DriverManager.getConnection("jdbc:sqlite:" + dbName)
        if (sqlite3_open(dbName.c_str(), &connection) != SQLITE_OK) {
            std::string msg = connection ? sqlite3_errmsg(connection)
                                         : "unable to open database: " + dbName;
            sqlite3_close(connection);
            connection = nullptr;
            throw std::runtime_error(msg); // stands in for SQLException
        }
        createTable();
    }

    ~BookManagementDB() {
        if (connection) sqlite3_close(connection);
    }

    BookManagementDB(const BookManagementDB&) = delete;
    BookManagementDB& operator=(const BookManagementDB&) = delete;

    void createTable() {
        const char* createTableSQL =
            "CREATE TABLE IF NOT EXISTS books ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT, "
            "author TEXT, "
            "available INTEGER"
            ")";
        StmtGuard stmt(prepare(createTableSQL));
        stepDone(stmt.get());
    }

    void addBook(const std::string& title, const std::string& author) {
        const char* insertSQL = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)";
        StmtGuard pstmt(prepare(insertSQL));
        bind(pstmt.get(), 1, title);
        bind(pstmt.get(), 2, author);
        stepDone(pstmt.get());
    }

    void removeBook(int bookId) {
        const char* deleteSQL = "DELETE FROM books WHERE id = ?";
        StmtGuard pstmt(prepare(deleteSQL));
        bind(pstmt.get(), 1, bookId);
        stepDone(pstmt.get());
    }

    void borrowBook(int bookId) {
        const char* updateSQL = "UPDATE books SET available = 0 WHERE id = ?";
        StmtGuard pstmt(prepare(updateSQL));
        bind(pstmt.get(), 1, bookId);
        stepDone(pstmt.get());
    }

    void returnBook(int bookId) {
        const char* updateSQL = "UPDATE books SET available = 1 WHERE id = ?";
        StmtGuard pstmt(prepare(updateSQL));
        bind(pstmt.get(), 1, bookId);
        stepDone(pstmt.get());
    }

    std::vector<Book> searchBooks() {
        const char* selectSQL = "SELECT * FROM books";
        std::vector<Book> books;
        StmtGuard stmt(prepare(selectSQL));
        int rc;
        while ((rc = sqlite3_step(stmt.get())) == SQLITE_ROW) {
            // Column order matches the table: id(0), title(1), author(2), available(3)
            int id = sqlite3_column_int(stmt.get(), 0);
            const unsigned char* titleText = sqlite3_column_text(stmt.get(), 1);
            const unsigned char* authorText = sqlite3_column_text(stmt.get(), 2);
            int available = sqlite3_column_int(stmt.get(), 3);
            std::string title = titleText ? reinterpret_cast<const char*>(titleText) : "";
            std::string author = authorText ? reinterpret_cast<const char*>(authorText) : "";
            books.emplace_back(id, title, author, available);
        }
        if (rc != SQLITE_DONE) {
            throw std::runtime_error(sqlite3_errmsg(connection));
        }
        return books;
    }

private:
    sqlite3* connection = nullptr;

    struct StmtGuard {
        sqlite3_stmt* stmt;
        explicit StmtGuard(sqlite3_stmt* s) : stmt(s) {}
        ~StmtGuard() { if (stmt) sqlite3_finalize(stmt); }
        StmtGuard(const StmtGuard&) = delete;
        StmtGuard& operator=(const StmtGuard&) = delete;
        sqlite3_stmt* get() const { return stmt; }
    };

    sqlite3_stmt* prepare(const char* sql) {
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            if (stmt) sqlite3_finalize(stmt);
            throw std::runtime_error(sqlite3_errmsg(connection));
        }
        return stmt;
    }

    void bind(sqlite3_stmt* stmt, int index, int value) {
        if (sqlite3_bind_int(stmt, index, value) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection));
        }
    }

    void bind(sqlite3_stmt* stmt, int index, const std::string& value) {
        if (sqlite3_bind_text(stmt, index, value.c_str(), -1, SQLITE_TRANSIENT) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection));
        }
    }

    void stepDone(sqlite3_stmt* stmt) {
        int rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            throw std::runtime_error(sqlite3_errmsg(connection));
        }
    }
};