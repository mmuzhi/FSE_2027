// BookManagementDB: a database class used as a book management system,
// handling the operations of adding, removing, updating, and searching books.
//
// Requires the SQLite3 C library (e.g. g++ -std=c++17 thisfile.cpp -lsqlite3).

#include <sqlite3.h>

#include <memory>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

// Equivalent of Python's sqlite3.Error (base of sqlite3.OperationalError etc.).
class SqliteError : public std::runtime_error {
public:
    explicit SqliteError(const std::string& message)
        : std::runtime_error(message) {}
};

class BookManagementDB {
public:
    // One row of the books table: (id, title, author, available).
    using BookRecord = std::tuple<int, std::string, std::string, int>;

    // Initializes the class by creating a database connection and cursor,
    // and creates the book table if it does not already exist.
    // db_name: the name of the db file.
    explicit BookManagementDB(const std::string& db_name) {
        sqlite3* handle = nullptr;
        if (sqlite3_open(db_name.c_str(), &handle) != SQLITE_OK) {
            const std::string message = (handle != nullptr)
                ? sqlite3_errmsg(handle)
                : "unable to open database file";
            if (handle != nullptr) {
                sqlite3_close(handle);
            }
            throw SqliteError(message);
        }
        connection = handle;
        try {
            create_table();
        } catch (...) {
            sqlite3_close(connection);
            connection = nullptr;
            throw;
        }
    }

    // Closes the database connection (Python closes it when the object is
    // garbage-collected).
    ~BookManagementDB() {
        sqlite3_close(connection);
    }

    BookManagementDB(const BookManagementDB&) = delete;
    BookManagementDB& operator=(const BookManagementDB&) = delete;

    BookManagementDB(BookManagementDB&& other) noexcept
        : connection(std::exchange(other.connection, nullptr)) {}

    BookManagementDB& operator=(BookManagementDB&& other) noexcept {
        if (this != &other) {
            sqlite3_close(connection);
            connection = std::exchange(other.connection, nullptr);
        }
        return *this;
    }

    // Creates the book table in the database if it does not already exist.
    void create_table() {
        execute(R"(
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                available INTEGER
            )
        )", [](sqlite3_stmt*) {});
    }

    // Adds a book to the database with the specified title and author,
    // setting its availability to 1 as free to borrow.
    void add_book(const std::string& title, const std::string& author) {
        execute(R"(
            INSERT INTO books (title, author, available)
            VALUES (?, ?, 1)
        )", [&](sqlite3_stmt* stmt) {
            bind_text(stmt, 1, title);
            bind_text(stmt, 2, author);
        });
    }

    // Removes a book from the database based on the given book ID.
    void remove_book(int book_id) {
        execute(R"(
            DELETE FROM books WHERE id = ?
        )", [&](sqlite3_stmt* stmt) { bind_int(stmt, 1, book_id); });
    }

    // Marks a book as borrowed in the database based on the given book ID.
    void borrow_book(int book_id) {
        execute(R"(
            UPDATE books SET available = 0 WHERE id = ?
        )", [&](sqlite3_stmt* stmt) { bind_int(stmt, 1, book_id); });
    }

    // Marks a book as returned in the database based on the given book ID.
    void return_book(int book_id) {
        execute(R"(
            UPDATE books SET available = 1 WHERE id = ?
        )", [&](sqlite3_stmt* stmt) { bind_int(stmt, 1, book_id); });
    }

    // Retrieves all books from the database and returns their information.
    // Returns one (id, title, author, available) record per book, e.g.
    //   BookManagementDB book_db("test.db");
    //   book_db.add_book("book1", "author");
    //   book_db.search_books();  // [(1, "book1", "author", 1)]
    std::vector<BookRecord> search_books() {
        sqlite3_stmt* raw_stmt = nullptr;
        if (sqlite3_prepare_v2(connection, R"(
            SELECT * FROM books
        )", -1, &raw_stmt, nullptr) != SQLITE_OK) {
            throw SqliteError(sqlite3_errmsg(connection));
        }
        std::unique_ptr<sqlite3_stmt, decltype(&sqlite3_finalize)> stmt(
            raw_stmt, &sqlite3_finalize);

        std::vector<BookRecord> books;
        int rc;
        while ((rc = sqlite3_step(stmt.get())) == SQLITE_ROW) {
            const unsigned char* title = sqlite3_column_text(stmt.get(), 1);
            const unsigned char* author = sqlite3_column_text(stmt.get(), 2);
            books.emplace_back(
                sqlite3_column_int(stmt.get(), 0),
                title != nullptr
                    ? std::string(reinterpret_cast<const char*>(title))
                    : std::string(),
                author != nullptr
                    ? std::string(reinterpret_cast<const char*>(author))
                    : std::string(),
                sqlite3_column_int(stmt.get(), 3));
        }
        if (rc != SQLITE_DONE) {
            throw SqliteError(sqlite3_errmsg(connection));
        }
        return books;
    }

private:
    sqlite3* connection = nullptr;

    // Prepares, binds, runs and finalizes a single SQL statement (the role of
    // Python's cursor.execute). The connection stays in SQLite's autocommit
    // mode, so each successful statement is committed immediately -- the same
    // persisted result as the explicit connection.commit() calls in Python.
    template <typename Binder>
    void execute(const char* sql, Binder&& bind) {
        sqlite3_stmt* raw_stmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &raw_stmt, nullptr) != SQLITE_OK) {
            throw SqliteError(sqlite3_errmsg(connection));
        }
        std::unique_ptr<sqlite3_stmt, decltype(&sqlite3_finalize)> stmt(
            raw_stmt, &sqlite3_finalize);

        bind(stmt.get());

        if (sqlite3_step(stmt.get()) != SQLITE_DONE) {
            throw SqliteError(sqlite3_errmsg(connection));
        }
    }

    void bind_text(sqlite3_stmt* stmt, int index, const std::string& value) const {
        if (sqlite3_bind_text(stmt, index, value.c_str(),
                              static_cast<int>(value.size()),
                              SQLITE_TRANSIENT) != SQLITE_OK) {
            throw SqliteError(sqlite3_errmsg(connection));
        }
    }

    void bind_int(sqlite3_stmt* stmt, int index, int value) const {
        if (sqlite3_bind_int(stmt, index, value) != SQLITE_OK) {
            throw SqliteError(sqlite3_errmsg(connection));
        }
    }
};