// Translation of the Python MovieTicketDB class (sqlite3) to C++.
// Requires SQLite3: #include <sqlite3.h> and link with -lsqlite3.

#include <sqlite3.h>

#include <cstddef>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

// Mirrors Python's sqlite3.Error / sqlite3.OperationalError, which are raised
// when connecting or executing SQL fails.
class SqliteError : public std::runtime_error {
public:
    explicit SqliteError(const std::string& message)
        : std::runtime_error(message) {}
};

// # This is a class for movie database operations, which allows for inserting
// movie information, searching for movie information by name, and deleting
// movie information by name.
class MovieTicketDB {
public:
    // One row of the "tickets" table:
    // (id, movie_name, theater_name, seat_number, customer_name)
    using TicketRow =
        std::tuple<long long, std::string, std::string, std::string, std::string>;

    // Initializes the MovieTicketDB object with the specified database name.
    // db_name: the name of the SQLite database.
    // Throws SqliteError if the database cannot be opened (like sqlite3.connect).
    explicit MovieTicketDB(const std::string& db_name) {
        if (sqlite3_open(db_name.c_str(), &connection_) != SQLITE_OK) {
            const std::string message =
                connection_ != nullptr ? sqlite3_errmsg(connection_)
                                       : "unable to open database file";
            if (connection_ != nullptr) {
                sqlite3_close(connection_);
                connection_ = nullptr;
            }
            throw SqliteError(message);
        }
        try {
            create_table();
        } catch (...) {
            // The destructor does not run when the constructor throws.
            sqlite3_close(connection_);
            connection_ = nullptr;
            throw;
        }
    }

    // The class owns a single SQLite connection; copying is not meaningful.
    MovieTicketDB(const MovieTicketDB&) = delete;
    MovieTicketDB& operator=(const MovieTicketDB&) = delete;

    MovieTicketDB(MovieTicketDB&& other) noexcept : connection_(other.connection_) {
        other.connection_ = nullptr;
    }

    MovieTicketDB& operator=(MovieTicketDB&& other) noexcept {
        if (this != &other) {
            if (connection_ != nullptr) {
                sqlite3_close(connection_);
            }
            connection_ = other.connection_;
            other.connection_ = nullptr;
        }
        return *this;
    }

    // Closes the connection when the object is destroyed.
    ~MovieTicketDB() {
        if (connection_ != nullptr) {
            sqlite3_close(connection_);
        }
    }

    // Creates a "tickets" table in the database if it does not exist already.
    // Fields: ID of type INTEGER, movie name, theater name, seat number and
    // customer name of type TEXT.
    void create_table() {
        const char* sql = R"SQL(
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY,
                movie_name TEXT,
                theater_name TEXT,
                seat_number TEXT,
                customer_name TEXT
            )
        )SQL";
        char* error_message = nullptr;
        if (sqlite3_exec(connection_, sql, nullptr, nullptr, &error_message) != SQLITE_OK) {
            const std::string message =
                error_message != nullptr ? error_message : sqlite3_errmsg(connection_);
            sqlite3_free(error_message);
            throw SqliteError(message);
        }
    }

    // Inserts a new ticket into the "tickets" table.
    void insert_ticket(const std::string& movie_name, const std::string& theater_name,
                       const std::string& seat_number, const std::string& customer_name) {
        StatementGuard statement(prepare(R"SQL(
            INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name)
            VALUES (?, ?, ?, ?)
        )SQL"));
        bind_text(statement.get(), 1, movie_name);
        bind_text(statement.get(), 2, theater_name);
        bind_text(statement.get(), 3, seat_number);
        bind_text(statement.get(), 4, customer_name);
        step_to_done(statement.get());
    }

    // Searches for tickets in the "tickets" table by customer name.
    // Returns the rows from the "tickets" table that match the search criteria.
    std::vector<TicketRow> search_tickets_by_customer(const std::string& customer_name) {
        StatementGuard statement(prepare(R"SQL(
            SELECT * FROM tickets WHERE customer_name = ?
        )SQL"));
        bind_text(statement.get(), 1, customer_name);

        std::vector<TicketRow> tickets;
        for (;;) {
            const int result = sqlite3_step(statement.get());
            if (result == SQLITE_ROW) {
                tickets.emplace_back(
                    sqlite3_column_int64(statement.get(), 0),
                    column_text(statement.get(), 1),
                    column_text(statement.get(), 2),
                    column_text(statement.get(), 3),
                    column_text(statement.get(), 4));
            } else if (result == SQLITE_DONE) {
                break;
            } else {
                throw SqliteError(sqlite3_errmsg(connection_));
            }
        }
        return tickets;
    }

    // Deletes a ticket from the "tickets" table by ticket ID.
    void delete_ticket(long long ticket_id) {
        StatementGuard statement(prepare(R"SQL(
            DELETE FROM tickets WHERE id = ?
        )SQL"));
        if (sqlite3_bind_int64(statement.get(), 1, ticket_id) != SQLITE_OK) {
            throw SqliteError(sqlite3_errmsg(connection_));
        }
        step_to_done(statement.get());
    }

private:
    // RAII wrapper that finalizes a prepared statement.
    class StatementGuard {
    public:
        explicit StatementGuard(sqlite3_stmt* statement) : statement_(statement) {}
        ~StatementGuard() { sqlite3_finalize(statement_); }
        StatementGuard(const StatementGuard&) = delete;
        StatementGuard& operator=(const StatementGuard&) = delete;
        sqlite3_stmt* get() const { return statement_; }

    private:
        sqlite3_stmt* statement_;
    };

    sqlite3_stmt* prepare(const char* sql) {
        sqlite3_stmt* statement = nullptr;
        if (sqlite3_prepare_v2(connection_, sql, -1, &statement, nullptr) != SQLITE_OK) {
            throw SqliteError(sqlite3_errmsg(connection_));
        }
        return statement;
    }

    void bind_text(sqlite3_stmt* statement, int index, const std::string& value) {
        if (sqlite3_bind_text(statement, index, value.c_str(),
                              static_cast<int>(value.size()),
                              SQLITE_TRANSIENT) != SQLITE_OK) {
            throw SqliteError(sqlite3_errmsg(connection_));
        }
    }

    void step_to_done(sqlite3_stmt* statement) {
        if (sqlite3_step(statement) != SQLITE_DONE) {
            throw SqliteError(sqlite3_errmsg(connection_));
        }
    }

    // NULL text columns (not producible through this class's API, which only
    // binds non-NULL strings) are read back as "".
    static std::string column_text(sqlite3_stmt* statement, int index) {
        const unsigned char* text = sqlite3_column_text(statement, index);
        if (text == nullptr) {
            return std::string();
        }
        const int bytes = sqlite3_column_bytes(statement, index);
        return std::string(reinterpret_cast<const char*>(text),
                           static_cast<std::size_t>(bytes));
    }

    sqlite3* connection_ = nullptr;
};