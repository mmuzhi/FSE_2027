#include <sqlite3.h>

#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

// Mirrors java.sql.SQLException
class SQLException : public std::runtime_error {
public:
    explicit SQLException(const std::string& message)
        : std::runtime_error(message) {}
};

class BookManagementDB {
private:
    // RAII wrapper mirroring Java's try-with-resources for statements
    struct StmtDeleter {
        void operator()(sqlite3_stmt* stmt) const {
            if (stmt) sqlite3_finalize(stmt);
        }
    };
    using StmtPtr = std::unique_ptr<sqlite3_stmt, StmtDeleter>;

    sqlite3* connection_ = nullptr;

    StmtPtr prepare(const std::string& sql) {
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection_, sql.c_str(), -1, &stmt, nullptr) !=
            SQLITE_OK) {
            throw SQLException(sqlite3_errmsg(connection_));
        }
        return StmtPtr(stmt);
    }

    // Mirrors prepare + bind int + executeUpdate
    void executeUpdateWithInt(const std::string& sql, int value) {
        StmtPtr pstmt = prepare(sql);
        if (sqlite3_bind_int(pstmt.get(), 1, value) != SQLITE_OK) {
            throw SQLException(sqlite3_errmsg(connection_));
        }
        if (sqlite3_step(pstmt.get()) != SQLITE_DONE) {
            throw SQLException(sqlite3_errmsg(connection_));
        }
    }

    // Mirrors ResultSet.getXxx(String columnLabel) lookup by name
    static int columnIndex(sqlite3_stmt* stmt, const char* name) {
        int count = sqlite3_column_count(stmt);
        for (int i = 0; i < count; ++i) {
            const char* col = sqlite3_column_name(stmt, i);
            if (col && name == std::string(col)) return i;
        }
        throw SQLException("no such column: " + std::string(name));
    }

    static std::string columnText(sqlite3_stmt* stmt, int index) {
        const unsigned char* text = sqlite3_column_text(stmt, index);
        return text ? reinterpret_cast<const char*>(text) : "";
    }

public:
    // Mirrors the Java static nested class Book
    class Book {
    public:
        Book(int id, std::string title, std::string author, int available)
            : id_(id), title_(std::move(title)), author_(std::move(author)),
              available_(available) {}

        int getId() const { return id_; }
        const std::string& getTitle() const { return title_; }
        const std::string& getAuthor() const { return author_; }
        int getAvailable() const { return available_; }

        std::string toString() const {
            return "Book{id=" + std::to_string(id_) +
                   ", title='" + title_ +
                   "', author='" + author_ +
                   "', available=" + std::to_string(available_) +
                   "}";
        }

    private:
        int id_;
        std::string title_;
        std::string author_;
        int available_;
    };

    explicit BookManagementDB(const std::string& dbName) {
        // Mirrors DriverManager.getConnection("jdbc:sqlite:" + dbName)
        if (sqlite3_open(dbName.c_str(), &connection_) != SQLITE_OK) {
            std::string msg = connection_
                ? sqlite3_errmsg(connection_)
                : "unable to open database: " + dbName;
            sqlite3_close(connection_);
            connection_ = nullptr;
            throw SQLException(msg);
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
        const char* createTableSQL =
            "CREATE TABLE IF NOT EXISTS books ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT, "
            "author TEXT, "
            "available INTEGER"
            ")";
        char* errMsg = nullptr;
        if (sqlite3_exec(connection_, createTableSQL, nullptr, nullptr,
                         &errMsg) != SQLITE_OK) {
            std::string msg = errMsg ? errMsg : sqlite3_errmsg(connection_);
            sqlite3_free(errMsg);
            throw SQLException(msg);
        }
    }

    void addBook(const std::string& title, const std::string& author) {
        const char* insertSQL =
            "INSERT INTO books (title, author, available) VALUES (?, ?, 1)";
        StmtPtr pstmt = prepare(insertSQL);
        if (sqlite3_bind_text(pstmt.get(), 1, title.c_str(), -1,
                              SQLITE_TRANSIENT) != SQLITE_OK ||
            sqlite3_bind_text(pstmt.get(), 2, author.c_str(), -1,
                              SQLITE_TRANSIENT) != SQLITE_OK) {
            throw SQLException(sqlite3_errmsg(connection_));
        }
        if (sqlite3_step(pstmt.get()) != SQLITE_DONE) {
            throw SQLException(sqlite3_errmsg(connection_));
        }
    }

    void removeBook(int bookId) {
        executeUpdateWithInt("DELETE FROM books WHERE id = ?", bookId);
    }

    void borrowBook(int bookId) {
        executeUpdateWithInt("UPDATE books SET available = 0 WHERE id = ?",
                             bookId);
    }

    void returnBook(int bookId) {
        executeUpdateWithInt("UPDATE books SET available = 1 WHERE id = ?",
                             bookId);
    }

    std::vector<Book> searchBooks() {
        const char* selectSQL = "SELECT * FROM books";
        std::vector<Book> books;
        StmtPtr stmt = prepare(selectSQL);
        sqlite3_stmt* rs = stmt.get();
        while (sqlite3_step(rs) == SQLITE_ROW) {
            int id = sqlite3_column_int(rs, columnIndex(rs, "id"));
            std::string title = columnText(rs, columnIndex(rs, "title"));
            std::string author = columnText(rs, columnIndex(rs, "author"));
            int available = sqlite3_column_int(rs, columnIndex(rs, "available"));
            books.emplace_back(id, title, author, available);
        }
        return books;
    }
};