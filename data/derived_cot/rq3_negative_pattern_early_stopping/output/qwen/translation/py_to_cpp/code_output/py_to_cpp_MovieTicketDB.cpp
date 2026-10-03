#include <sqlite3.h>
#include <string>
#include <vector>
#include <tuple>
#include <stdexcept>

class MovieTicketDB {
private:
    sqlite3* db;
    sqlite3_stmt* stmt;
    std::string dbName;

    bool open(const std::string& db_name) {
        int rc = sqlite3_open(db_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            return false;
        }
        return true;
    }

public:
    MovieTicketDB(const std::string& db_name) : db(nullptr), stmt(nullptr), dbName(db_name) {
        if (!open(dbName)) {
            throw std::runtime_error("Failed to open database");
        }
        create_table();
    }

    ~MovieTicketDB() {
        if (db) {
            sqlite3_close(db);
        }
        if (stmt) {
            sqlite3_finalize(stmt);
        }
    }

    void create_table() {
        const char* sql = "CREATE TABLE IF NOT EXISTS tickets ("
            "id INTEGER PRIMARY KEY,"
            "movie_name TEXT,"
            "theater_name TEXT,"
            "seat_number TEXT,"
            "customer_name TEXT"
            ");";
        int rc = sqlite3_exec(db, sql, nullptr, nullptr, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db));
        }
    }

    void insert_ticket(const std::string& movie_name, const std::string& theater_name, const std::string& seat_number, const std::string& customer_name) {
        const char* sql = "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) VALUES (?, ?, ?, ?)";
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db));
        }

        sqlite3_bind_text(stmt, 1, movie_name.c_str(), movie_name.size(), SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, theater_name.c_str(), theater_name.size(), SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, seat_number.c_str(), seat_number.size(), SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 4, customer_name.c_str(), customer_name.size(), SQLITE_TRANSIENT);

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            throw std::runtime_error(sqlite3_errmsg(db));
        }

        sqlite3_finalize(stmt);
    }

    std::vector<std::tuple<int, std::string, std::string, std::string, std::string>> search_tickets_by_customer(const std::string& customer_name) {
        const char* sql = "SELECT * FROM tickets WHERE customer_name = ?";
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db));
        }

        sqlite3_bind_text(stmt, 1, customer_name.c_str(), customer_name.size(), SQLITE_TRANSIENT);

        std::vector<std::tuple<int, std::string, std::string, std::string, std::string>> results;
        while (sqlite3_step(stmt) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const char* movie_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            const char* theater_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
            const char* seat_number = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3));
            const char* customer_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));

            results.emplace_back(
                id,
                movie_name,
                theater_name,
                seat_number,
                customer_name
            );
        }

        sqlite3_finalize(stmt);
        return results;
    }

    void delete_ticket(int ticket_id) {
        const char* sql = "DELETE FROM tickets WHERE id = ?";
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db));
        }

        sqlite3_bind_int(stmt, 1, ticket_id);

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            throw std::runtime_error(sqlite3_errmsg(db));
        }

        sqlite3_finalize(stmt);
    }
};