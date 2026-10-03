#include <sqlite3.h>
#include <vector>
#include <string>
#include <cstdio>
#include <stdexcept>

struct MovieTicketDB {
    sqlite3* db;
    MovieTicketDB(const std::string& dbName) {
        if (sqlite3_open(dbName.c_str(), &db) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db));
        }
        createTable();
    }

    ~MovieTicketDB() {
        sqlite3_close(db);
    }

    void createTable() {
        const char* sql = "CREATE TABLE IF NOT EXISTS tickets (" \
                          "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                          "movie_name TEXT, " \
                          "theater_name TEXT, " \
                          "seat_number TEXT, " \
                          "customer_name TEXT)";
        char* errMsg = nullptr;
        if (sqlite3_exec(db, sql, nullptr, nullptr, &errMsg) != SQLITE_OK) {
            fprintf(stderr, "SQL error: %s\n", errMsg);
            sqlite3_free(errMsg);
            throw std::runtime_error("Table creation failed");
        }
    }

    void insertTicket(const std::string& movieName, const std::string& theaterName, 
                     const std::string& seatNumber, const std::string& customerName) {
        const char* sql = "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) VALUES (?, ?, ?, ?)";
        sqlite3_stmt* stmt;
        if (sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            fprintf(stderr, "SQL error: %s\n", sqlite3_errmsg(db));
            throw std::runtime_error("Prepare failed");
        }

        sqlite3_bind_text(stmt, 1, movieName.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 2, theaterName.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 3, seatNumber.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_text(stmt, 4, customerName.c_str(), -1, SQLITE_STATIC);

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            fprintf(stderr, "SQL error: %s\n", sqlite3_errmsg(db));
            throw std::runtime_error("Insert failed");
        }

        sqlite3_finalize(stmt);
    }

    std::vector<Ticket> searchTicketsByCustomer(const std::string& customerName) {
        std::vector<Ticket> tickets;
        const char* sql = "SELECT * FROM tickets WHERE customer_name = ?";
        sqlite3_stmt* stmt;
        if (sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            fprintf(stderr, "SQL error: %s\n", sqlite3_errmsg(db));
            throw std::runtime_error("Prepare failed");
        }

        sqlite3_bind_text(stmt, 1, customerName.c_str(), -1, SQLITE_STATIC);

        while (sqlite3_step(stmt) == SQLITE_ROW) {
            Ticket ticket(
                sqlite3_column_int(stmt, 0),
                reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)),
                reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2)),
                reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3)),
                reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4))
            );
            tickets.push_back(ticket);
        }

        sqlite3_finalize(stmt);
        return tickets;
    }

    void deleteTicket(int ticketId) {
        const char* sql = "DELETE FROM tickets WHERE id = ?";
        sqlite3_stmt* stmt;
        if (sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            fprintf(stderr, "SQL error: %s\n", sqlite3_errmsg(db));
            throw std::runtime_error("Prepare failed");
        }

        sqlite3_bind_int(stmt, 1, ticketId);

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            fprintf(stderr, "SQL error: %s\n", sqlite3_errmsg(db));
            throw std::runtime_error("Delete failed");
        }

        sqlite3_finalize(stmt);
    }

    struct Ticket {
        int id;
        std::string movieName;
        std::string theaterName;
        std::string seatNumber;
        std::string customerName;

        Ticket(int id, const char* movieName, const char* theaterName, 
               const char* seatNumber, const char* customerName)
            : id(id), movieName(movieName), theaterName(theaterName),
              seatNumber(seatNumber), customerName(customerName) {}
    };
};