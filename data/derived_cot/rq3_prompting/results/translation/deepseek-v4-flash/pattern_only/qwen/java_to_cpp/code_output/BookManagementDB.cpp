#include <sqlite3.h>
#include <string>
#include <vector>
#include <stdexcept>
#include <sstream>

class BookManagementDB {
private:
    sqlite3* connection;

    void ensure_ok(int rc, const std::string& msg) const {
        if (rc != SQLITE_OK) {
            throw std::runtime_error(msg + ": " + sqlite3_errmsg(connection));
        }
    }

    void createTable() {
        const std::string sql =
            "CREATE TABLE IF NOT EXISTS books ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT, "
            "author TEXT, "
            "available INTEGER"
            ")";
        char* errMsg = nullptr;
        int rc = sqlite3_exec(connection, sql.c_str(), nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::string message = "Failed to create table";
            if (errMsg) {
                message += ": ";
                message += errMsg;
                sqlite3_free(errMsg);
            }
            throw std::runtime_error(message);
        }
    }

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
        std::string getTitle() const { return title; }
        std::string getAuthor() const { return author; }
        int getAvailable() const { return available; }

        std::string toString() const {
            std::ostringstream oss;
            oss << "Book{id=" << id
                << ", title='" << title
                << "', author='" << author
                << "', available=" << available
                << "}";
            return oss.str();
        }
    };

    BookManagementDB(const std::string& dbName) {
        int rc = sqlite3_open(dbName.c_str(), &connection);
        if (rc != SQLITE_OK) {
            std::string msg = "Cannot open database: ";
            msg += sqlite3_errmsg(connection);
            sqlite3_close(connection);
            throw std::runtime_error(msg);
        }
        createTable();
    }

    ~BookManagementDB() {
        if (connection) {
            sqlite3_close(connection);
        }
    }

    BookManagementDB(const BookManagementDB&) = delete;
    BookManagementDB& operator=(const BookManagementDB&) = delete;

    void addBook(const std::string& title, const std::string& author) {
        const std::string sql = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, sql.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare addBook: " + std::string(sqlite3_errmsg(connection)));
        }
        rc = sqlite3_bind_text(stmt, 1, title.c_str(), -1, SQLITE_TRANSIENT);
        if (rc != SQLITE_OK) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to bind title: " + std::string(sqlite3_errmsg(connection)));
        }
        rc = sqlite3_bind_text(stmt, 2, author.c_str(), -1, SQLITE_TRANSIENT);
        if (rc != SQLITE_OK) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to bind author: " + std::string(sqlite3_errmsg(connection)));
        }
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to execute addBook: " + std::string(sqlite3_errmsg(connection)));
        }
        sqlite3_finalize(stmt);
    }

    void removeBook(int bookId) {
        const std::string sql = "DELETE FROM books WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, sql.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare removeBook: " + std::string(sqlite3_errmsg(connection)));
        }
        rc = sqlite3_bind_int(stmt, 1, bookId);
        if (rc != SQLITE_OK) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to bind id: " + std::string(sqlite3_errmsg(connection)));
        }
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to execute removeBook: " + std::string(sqlite3_errmsg(connection)));
        }
        sqlite3_finalize(stmt);
    }

    void borrowBook(int bookId) {
        const std::string sql = "UPDATE books SET available = 0 WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, sql.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare borrowBook: " + std::string(sqlite3_errmsg(connection)));
        }
        rc = sqlite3_bind_int(stmt, 1, bookId);
        if (rc != SQLITE_OK) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to bind id: " + std::string(sqlite3_errmsg(connection)));
        }
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to execute borrowBook: " + std::string(sqlite3_errmsg(connection)));
        }
        sqlite3_finalize(stmt);
    }

    void returnBook(int bookId) {
        const std::string sql = "UPDATE books SET available = 1 WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, sql.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare returnBook: " + std::string(sqlite3_errmsg(connection)));
        }
        rc = sqlite3_bind_int(stmt, 1, bookId);
        if (rc != SQLITE_OK) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to bind id: " + std::string(sqlite3_errmsg(connection)));
        }
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to execute returnBook: " + std::string(sqlite3_errmsg(connection)));
        }
        sqlite3_finalize(stmt);
    }

    std::vector<Book> searchBooks() {
        const std::string sql = "SELECT * FROM books";
        std::vector<Book> books;
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, sql.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare searchBooks: " + std::string(sqlite3_errmsg(connection)));
        }

        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const unsigned char* titleText = sqlite3_column_text(stmt, 1);
            const unsigned char* authorText = sqlite3_column_text(stmt, 2);
            int available = sqlite3_column_int(stmt, 3);

            std::string title = titleText ? reinterpret_cast<const char*>(titleText) : "";
            std::string author = authorText ? reinterpret_cast<const char*>(authorText) : "";
            books.emplace_back(id, title, author, available);
        }

        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to execute searchBooks: " + std::string(sqlite3_errmsg(connection)));
        }

        sqlite3_finalize(stmt);
        return books;
    }
};