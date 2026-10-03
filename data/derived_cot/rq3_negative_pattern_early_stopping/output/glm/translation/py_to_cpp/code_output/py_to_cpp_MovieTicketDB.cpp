#include <string>
#include <vector>
#include <tuple>
#include <optional>
#include <sqlite3.h>
#include <stdexcept>

class MovieTicketDB {
private:
    sqlite3* connection;

    std::optional<std::string> get_column_text(sqlite3_stmt* stmt, int col) {
        const char* text = reinterpret_cast<const char*>(sqlite3_column_text(stmt, col));
        if (text) {
            return std::string(text);
        }
        return std::nullopt;
    }

public:
    using Ticket = std::tuple<int, std::optional<std::string>, std::optional<std::string>, std::optional<std::string>, std::optional<std::string>>;

    MovieTicketDB(const std::string& db_name) {
        int rc = sqlite3_open(db_name.c_str(), &connection);
        if (rc != SQLITE_OK) {
            std::string err_msg = "Cannot open database: " + std::string(sqlite3_errmsg(connection));
            sqlite3_close(connection);
            throw std::runtime_error(err_msg);
        }
        create_table();
    }

    ~MovieTicketDB() {
        if (connection) {
            sqlite3_close(connection);
        }
    }

    MovieTicketDB(const MovieTicketDB&) = delete;
    MovieTicketDB& operator=(const MovieTicketDB&) = delete;

    MovieTicketDB(MovieTicketDB&& other) noexcept : connection(other.connection) {
        other.connection = nullptr;
    }

    MovieTicketDB& operator=(MovieTicketDB&& other) noexcept {
        if (this != &other) {
            if (connection) {
                sqlite3_close(connection);
            }
            connection = other.connection;
            other.connection = nullptr;
        }
        return *this;
    }

    void create_table() {
        const char* sql = R"(
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY,
                movie_name TEXT,
                theater_name TEXT,
                seat_number TEXT,
                customer_name TEXT
            )
        )";
        char* err_msg = nullptr;
        int rc = sqlite3_exec(connection, sql, nullptr, nullptr, &err_msg);
        if (rc != SQLITE_OK) {
            std::string err_str = err_msg;
            sqlite3_free(err_msg);
            throw std::runtime_error("SQL error: " + err_str);
        }
    }

    void insert_ticket(const std::string& movie_name, const std::string& theater_name, const std::string& seat_number, const std::string& customer_name) {
        const char* sql = "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) VALUES (?, ?, ?, ?)";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare statement: " + std::string(sqlite3_errmsg(connection)));
        }

        sqlite3_bind_text(stmt, 1, movie_name.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, theater_name.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, seat_number.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 4, customer_name.c_str(), -1, SQLITE_TRANSIENT);

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::string err_msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to execute statement: " + err_msg);
        }
        sqlite3_finalize(stmt);
    }

    std::vector<Ticket> search_tickets_by_customer(const std::string& customer_name) {
        const char* sql = "SELECT * FROM tickets WHERE customer_name = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare statement: " + std::string(sqlite3_errmsg(connection)));
        }

        sqlite3_bind_text(stmt, 1, customer_name.c_str(), -1, SQLITE_TRANSIENT);

        std::vector<Ticket> tickets;
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            auto movie_name = get_column_text(stmt, 1);
            auto theater_name = get_column_text(stmt, 2);
            auto seat_number = get_column_text(stmt, 3);
            auto customer_name_row = get_column_text(stmt, 4);
            tickets.emplace_back(id, movie_name, theater_name, seat_number, customer_name_row);
        }

        if (rc != SQLITE_DONE) {
            std::string err_msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to execute statement: " + err_msg);
        }
        sqlite3_finalize(stmt);

        return tickets;
    }

    void delete_ticket(int ticket_id) {
        const char* sql = "DELETE FROM tickets WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare statement: " + std::string(sqlite3_errmsg(connection)));
        }

        sqlite3_bind_int(stmt, 1, ticket_id);

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::string err_msg = sqlite3_errmsg(connection);
            sqlite3_finalize(stmt);
            throw std::runtime_error("Failed to execute statement: " + err_msg);
        }
        sqlite3_finalize(stmt);
    }
};