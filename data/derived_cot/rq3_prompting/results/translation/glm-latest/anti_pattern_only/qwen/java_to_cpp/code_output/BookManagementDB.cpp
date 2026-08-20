#include <sqlite3.h>

#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace org {
namespace example {

class SQLException : public std::runtime_error {
public:
    explicit SQLException(const std::string& message)
        : std::runtime_error(message) {}
};

class BookManagementDB {
public:
    class Book {
    public:
        Book(int id, std::string title, std::string author, int available)
            : id_(id),
              title_(std::move(title)),
              author_(std::move(author)),
              available_(available) {}

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

    private:
        int id_;
        std::string title_;
        std::string author_;
        int available_;
    };

    explicit BookManagementDB(const std::string& dbName) {
        if (sqlite3_open(dbName.c_str(), &connection_) != SQLITE_OK) {
            std::string message = (connection_ != nullptr)
                                      ? sqlite3_errmsg(connection_)
                                      : "unable to open database: " + dbName;
            sqlite3_close(connection_);
            connection_ = nullptr;
            throw SQLException(message);
        }
        createTable();
    }

    ~BookManagementDB() {
        if (connection_ != nullptr) {
            sqlite3_close(connection_);
        }
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
        char* errorMessage = nullptr;
        if (sqlite3_exec(connection_, createTableSQL, nullptr, nullptr,
                         &errorMessage) != SQLITE_OK) {
            std::string message = (errorMessage != nullptr)
                                      ? errorMessage
                                      : sqlite3_errmsg(connection_);
            sqlite3_free(errorMessage);
            throw SQLException(message);
        }
    }

    void addBook(const std::string& title, const std::string& author) {
        const char* insertSQL =
            "INSERT INTO books (title, author, available) VALUES (?, ?, 1)";
        StatementGuard pstmt(prepare(insertSQL));
        bindText(pstmt.get(), 1, title);
        bindText(pstmt.get(), 2, author);
        executeUpdate(pstmt.get());
    }

    void removeBook(int bookId) {
        const char* deleteSQL = "DELETE FROM books WHERE id = ?";
        StatementGuard pstmt(prepare(deleteSQL));
        bindInt(pstmt.get(), 1, bookId);
        executeUpdate(pstmt.get());
    }

    void borrowBook(int bookId) {
        const char* updateSQL = "UPDATE books SET available = 0 WHERE id = ?";
        StatementGuard pstmt(prepare(updateSQL));
        bindInt(pstmt.get(), 1, bookId);
        executeUpdate(pstmt.get());
    }

    void returnBook(int bookId) {
        const char* updateSQL = "UPDATE books SET available = 1 WHERE id = ?";
        StatementGuard pstmt(prepare(updateSQL));
        bindInt(pstmt.get(), 1, bookId);
        executeUpdate(pstmt.get());
    }

    std::vector<Book> searchBooks() {
        const char* selectSQL = "SELECT * FROM books";
        std::vector<Book> books;
        StatementGuard stmt(prepare(selectSQL));
        int rc;
        while ((rc = sqlite3_step(stmt.get())) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt.get(), columnIndex(stmt.get(), "id"));
            std::string title = columnText(stmt.get(), columnIndex(stmt.get(), "title"));
            std::string author = columnText(stmt.get(), columnIndex(stmt.get(), "author"));
            int available =
                sqlite3_column_int(stmt.get(), columnIndex(stmt.get(), "available"));
            books.emplace_back(id, std::move(title), std::move(author), available);
        }
        if (rc != SQLITE_DONE) {
            throw SQLException(sqlite3_errmsg(connection_));
        }
        return books;
    }

private:
    sqlite3* connection_ = nullptr;

    // RAII wrapper replacing Java's try-with-resources on Statement/PreparedStatement.
    class StatementGuard {
    public:
        explicit StatementGuard(sqlite3_stmt* stmt) : stmt_(stmt) {}
        ~StatementGuard() { sqlite3_finalize(stmt_); }
        StatementGuard(const StatementGuard&) = delete;
        StatementGuard& operator=(const StatementGuard&) = delete;
        sqlite3_stmt* get() const { return stmt_; }

    private:
        sqlite3_stmt* stmt_;
    };

    sqlite3_stmt* prepare(const char* sql) {
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection_, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw SQLException(sqlite3_errmsg(connection_));
        }
        return stmt;
    }

    void bindText(sqlite3_stmt* stmt, int index, const std::string& value) {
        if (sqlite3_bind_text(stmt, index, value.c_str(), -1,
                              SQLITE_TRANSIENT) != SQLITE_OK) {
            throw SQLException(sqlite3_errmsg(connection_));
        }
    }

    void bindInt(sqlite3_stmt* stmt, int index, int value) {
        if (sqlite3_bind_int(stmt, index, value) != SQLITE_OK) {
            throw SQLException(sqlite3_errmsg(connection_));
        }
    }

    void executeUpdate(sqlite3_stmt* stmt) {
        int rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE && rc != SQLITE_ROW) {
            throw SQLException(sqlite3_errmsg(connection_));
        }
    }

    // Mirrors ResultSet.getXxx(String columnLabel) lookup by name.
    static int columnIndex(sqlite3_stmt* stmt, const char* columnName) {
        int count = sqlite3_column_count(stmt);
        for (int i = 0; i < count; ++i) {
            const char* name = sqlite3_column_name(stmt, i);
            if (name != nullptr && std::string(name) == columnName) {
                return i;
            }
        }
        throw SQLException("column not found: " + std::string(columnName));
    }

    static std::string columnText(sqlite3_stmt* stmt, int index) {
        const unsigned char* text = sqlite3_column_text(stmt, index);
        return (text != nullptr)
                   ? std::string(reinterpret_cast<const char*>(text))
                   : std::string();
    }
};

}  // namespace example
}  // namespace org