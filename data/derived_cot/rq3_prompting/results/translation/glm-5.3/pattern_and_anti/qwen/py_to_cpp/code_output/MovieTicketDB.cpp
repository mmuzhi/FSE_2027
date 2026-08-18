#include <sqlite3.h>
#include <string>
#include <vector>
#include <tuple>
#include <stdexcept>

class MovieTicketDB {
private:
    sqlite3* connection;

    static std::string column_text(sqlite3_stmt* stmt, int col) {
        const unsigned char* text = sqlite3_column_text(stmt, col);
        return text ? reinterpret_cast<const char*>(text) : std::string();
    }

public:
    explicit MovieTicketDB(const std::string& db_name) {
        if (sqlite3_open(db_name.c_str(), &connection) != SQLITE_OK) {
            std::string err = connection ? sqlite3_errmsg(connection) : "unknown error";
            if (connection) sqlite3_close(connection);
            connection = nullptr;
            throw std::runtime_error("Unable to connect to database: " + err);
        }
        create_table();
    }

    ~MovieTicketDB() {
        if (connection) sqlite3_close(connection);
    }

    MovieTicketDB(const MovieTicketDB&) = delete;
    MovieTicketDB& operator=(const MovieTicketDB&) = delete;

    void create_table() {
        const char* sql =
            "CREATE TABLE IF NOT EXISTS tickets ("
            "id INTEGER PRIMARY KEY, "
            "movie_name TEXT, "
            "theater_name TEXT, "
            "seat_number TEXT, "
            "customer_name TEXT"
            ")";
        char* err = nullptr;
        if (sqlite3_exec(connection, sql, nullptr, nullptr, &err) != SQLITE_OK) {
            std::string msg = err ? err : "unknown error";
            sqlite3_free(err);
            throw std::runtime_error("create_table failed: " + msg);
        }
    }

    void insert_ticket(const std::string& movie_name, const std::string& theater_name,
                       const std::string& seat_number, const std::string& customer_name) {
        const char* sql =
            "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) "
            "VALUES (?, ?, ?, ?)";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(std::string("insert_ticket failed: ") + sqlite3_errmsg(connection));
        }
        sqlite3_bind_text(stmt, 1, movie_name.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, theater_name.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, seat_number.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 4, customer_name.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error("insert_ticket failed: " + msg);
        }
        sqlite3_finalize(stmt);
    }

    std::vector<std::tuple<int, std::string, std::string, std::string, std::string>>
    search_tickets_by_customer(const std::string& customer_name) {
        const char* sql = "SELECT * FROM tickets WHERE customer_name = ?";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(std::string("search_tickets_by_customer failed: ") + sqlite3_errmsg(connection));
        }
        sqlite3_bind_text(stmt, 1, customer_name.c_str(), -1, SQLITE_TRANSIENT);

        std::vector<std::tuple<int, std::string, std::string, std::string, std::string>> tickets;
        int rc;
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            tickets.emplace_back(
                sqlite3_column_int(stmt, 0),
                column_text(stmt, 1),
                column_text(stmt, 2),
                column_text(stmt, 3),
                column_text(stmt, 4)
            );
        }
        if (rc != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error("search_tickets_by_customer failed: " + msg);
        }
        sqlite3_finalize(stmt);
        return tickets;
    }

    void delete_ticket(int ticket_id) {
        const char* sql = "DELETE FROM tickets WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(std::string("delete_ticket failed: ") + sqlite3_errmsg(connection));
        }
        sqlite3_bind_int(stmt, 1, ticket_id);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error("delete_ticket failed: " + msg);
        }
        sqlite3_finalize(stmt);
    }
};