#include <sqlite3.h>
#include <string>
#include <vector>
#include <tuple>
#include <stdexcept>
#include <cstring>

class MovieTicketDB {
private:
    sqlite3* connection;

    // Helper to throw an exception with the last SQLite error message
    void throw_sqlite_error(const std::string& context) {
        std::string msg = context + ": " + sqlite3_errmsg(connection);
        throw std::runtime_error(msg);
    }

public:
    // Opens the database and creates the table if it does not exist.
    MovieTicketDB(const std::string& db_name) {
        int rc = sqlite3_open(db_name.c_str(), &connection);
        if (rc != SQLITE_OK) {
            std::string msg = "Failed to open database: " + std::string(sqlite3_errmsg(connection));
            sqlite3_close(connection);
            throw std::runtime_error(msg);
        }
        create_table();
    }

    // Destructor closes the database connection.
    ~MovieTicketDB() {
        if (connection) {
            sqlite3_close(connection);
        }
    }

    // Creates the "tickets" table if it does not exist yet.
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
        char* errMsg = nullptr;
        int rc = sqlite3_exec(connection, sql, nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::string msg = "Failed to create table: " + std::string(errMsg);
            sqlite3_free(errMsg);
            throw std::runtime_error(msg);
        }
    }

    // Inserts a new ticket into the table.
    void insert_ticket(const std::string& movie_name,
                       const std::string& theater_name,
                       const std::string& seat_number,
                       const std::string& customer_name) {
        const char* sql = "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) "
                          "VALUES (?, ?, ?, ?)";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) throw_sqlite_error("Failed to prepare INSERT");

        // Bind parameters
        sqlite3_bind_text(stmt, 1, movie_name.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, theater_name.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, seat_number.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 4, customer_name.c_str(), -1, SQLITE_TRANSIENT);

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw_sqlite_error("Failed to execute INSERT");
        }
        sqlite3_finalize(stmt);
    }

    // Searches for tickets by customer name and returns a list of rows.
    std::vector<std::tuple<int, std::string, std::string, std::string, std::string>>
    search_tickets_by_customer(const std::string& customer_name) {
        const char* sql = "SELECT * FROM tickets WHERE customer_name = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) throw_sqlite_error("Failed to prepare SELECT");

        sqlite3_bind_text(stmt, 1, customer_name.c_str(), -1, SQLITE_TRANSIENT);

        std::vector<std::tuple<int, std::string, std::string, std::string, std::string>> results;
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const char* movie_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            const char* theater_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
            const char* seat_number = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3));
            const char* customer = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));
            results.emplace_back(
                id,
                movie_name ? movie_name : "",
                theater_name ? theater_name : "",
                seat_number ? seat_number : "",
                customer ? customer : ""
            );
        }
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw_sqlite_error("Failed to step through SELECT results");
        }
        sqlite3_finalize(stmt);
        return results;
    }

    // Deletes a ticket by its ID.
    void delete_ticket(int ticket_id) {
        const char* sql = "DELETE FROM tickets WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) throw_sqlite_error("Failed to prepare DELETE");

        sqlite3_bind_int(stmt, 1, ticket_id);

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            sqlite3_finalize(stmt);
            throw_sqlite_error("Failed to execute DELETE");
        }
        sqlite3_finalize(stmt);
    }
};