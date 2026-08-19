#include <sqlite3.h>

#include <cstdint>
#include <optional>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

// Mirrors Python's sqlite3-based MovieTicketDB: each statement runs in
// autocommit mode (SQLite default), matching the committed state after
// each Python connection.commit(). Errors raise like sqlite3 exceptions.
class MovieTicketDB {
public:
    // A row: (id, movie_name, theater_name, seat_number, customer_name).
    // NULL text columns map to std::nullopt (Python's None).
    using TicketRow = std::tuple<std::int64_t,
                                 std::optional<std::string>,
                                 std::optional<std::string>,
                                 std::optional<std::string>,
                                 std::optional<std::string>>;

    explicit MovieTicketDB(const std::string& db_name)
        : connection_(nullptr) {
        if (sqlite3_open(db_name.c_str(), &connection_) != SQLITE_OK) {
            const std::string msg = connection_
                                        ? sqlite3_errmsg(connection_)
                                        : "unable to open database file";
            sqlite3_close(connection_);
            connection_ = nullptr;
            throw std::runtime_error(msg);
        }
        create_table();
    }

    ~MovieTicketDB() {
        if (connection_ != nullptr) {
            sqlite3_close(connection_);
        }
    }

    MovieTicketDB(const MovieTicketDB&) = delete;
    MovieTicketDB& operator=(const MovieTicketDB&) = delete;

    void create_table() {
        execute("CREATE TABLE IF NOT EXISTS tickets ("
                "id INTEGER PRIMARY KEY, "
                "movie_name TEXT, "
                "theater_name TEXT, "
                "seat_number TEXT, "
                "customer_name TEXT"
                ")");
    }

    void insert_ticket(const std::string& movie_name,
                       const std::string& theater_name,
                       const std::string& seat_number,
                       const std::string& customer_name) {
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection_,
                               "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) "
                               "VALUES (?, ?, ?, ?)",
                               -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        bind_text(stmt, 1, movie_name);
        bind_text(stmt, 2, theater_name);
        bind_text(stmt, 3, seat_number);
        bind_text(stmt, 4, customer_name);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_finalize(stmt);
    }

    std::vector<TicketRow> search_tickets_by_customer(const std::string& customer_name) {
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection_,
                               "SELECT * FROM tickets WHERE customer_name = ?",
                               -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        bind_text(stmt, 1, customer_name);

        std::vector<TicketRow> tickets;
        int rc = sqlite3_step(stmt);
        while (rc == SQLITE_ROW) {
            tickets.emplace_back(sqlite3_column_int64(stmt, 0),
                                 column_text(stmt, 1),
                                 column_text(stmt, 2),
                                 column_text(stmt, 3),
                                 column_text(stmt, 4));
            rc = sqlite3_step(stmt);
        }
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_finalize(stmt);
        return tickets;
    }

    void delete_ticket(std::int64_t ticket_id) {
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection_,
                               "DELETE FROM tickets WHERE id = ?",
                               -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_bind_int64(stmt, 1, ticket_id);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw std::runtime_error(sqlite3_errmsg(connection_));
        }
        sqlite3_finalize(stmt);
    }

private:
    sqlite3* connection_;

    void execute(const char* sql) {
        char* err_msg = nullptr;
        if (sqlite3_exec(connection_, sql, nullptr, nullptr, &err_msg) != SQLITE_OK) {
            const std::string msg = err_msg != nullptr ? err_msg : "database error";
            sqlite3_free(err_msg);
            throw std::runtime_error(msg);
        }
    }

    static void bind_text(sqlite3_stmt* stmt, int index, const std::string& value) {
        if (sqlite3_bind_text(stmt, index, value.c_str(), -1, SQLITE_TRANSIENT) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(sqlite3_db_handle(stmt)));
        }
    }

    static std::optional<std::string> column_text(sqlite3_stmt* stmt, int col) {
        const unsigned char* text = sqlite3_column_text(stmt, col);
        if (text == nullptr) {
            return std::nullopt;
        }
        return std::string(reinterpret_cast<const char*>(text));
    }
};