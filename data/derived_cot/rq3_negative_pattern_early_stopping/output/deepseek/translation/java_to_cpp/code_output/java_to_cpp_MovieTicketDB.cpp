#include <sqlite3.h>
#include <iostream>
#include <string>
#include <vector>
#include <stdexcept>

class MovieTicketDB {
private:
    sqlite3* db;

    void createTable() {
        const char* sql = "CREATE TABLE IF NOT EXISTS tickets ("
                          "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                          "movie_name TEXT, "
                          "theater_name TEXT, "
                          "seat_number TEXT, "
                          "customer_name TEXT)";
        char* errMsg = nullptr;
        if (sqlite3_exec(db, sql, nullptr, nullptr, &errMsg) != SQLITE_OK) {
            std::cerr << "SQL error: " << errMsg << std::endl;
            sqlite3_free(errMsg);
        }
    }

public:
    MovieTicketDB(const std::string& dbName) : db(nullptr) {
        if (sqlite3_open(dbName.c_str(), &db) != SQLITE_OK) {
            std::cerr << "Can't open database: " << sqlite3_errmsg(db) << std::endl;
            sqlite3_close(db);
            db = nullptr;
            return;
        }
        createTable();
    }

    ~MovieTicketDB() {
        close();
    }

    void insertTicket(const std::string& movieName, const std::string& theaterName,
                      const std::string& seatNumber, const std::string& customerName) {
        const char* sql = "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) VALUES (?, ?, ?, ?)";
        sqlite3_stmt* stmt;
        if (sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            std::cerr << "Failed to prepare statement: " << sqlite3_errmsg(db) << std::endl;
            return;
        }
        sqlite3_bind_text(stmt, 1, movieName.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, theaterName.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, seatNumber.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 4, customerName.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::cerr << "Failed to execute insert: " << sqlite3_errmsg(db) << std::endl;
        }
        sqlite3_finalize(stmt);
    }

    struct Ticket {
        int id;
        std::string movieName;
        std::string theaterName;
        std::string seatNumber;
        std::string customerName;

        Ticket(int id, const std::string& movieName, const std::string& theaterName,
               const std::string& seatNumber, const std::string& customerName)
            : id(id), movieName(movieName), theaterName(theaterName), seatNumber(seatNumber), customerName(customerName) {}

        int getId() const { return id; }
        const std::string& getMovieName() const { return movieName; }
        const std::string& getTheaterName() const { return theaterName; }
        const std::string& getSeatNumber() const { return seatNumber; }
        const std::string& getCustomerName() const { return customerName; }
    };

    std::vector<Ticket> searchTicketsByCustomer(const std::string& customerName) {
        std::vector<Ticket> tickets;
        const char* sql = "SELECT * FROM tickets WHERE customer_name = ?";
        sqlite3_stmt* stmt;
        if (sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            std::cerr << "Failed to prepare statement: " << sqlite3_errmsg(db) << std::endl;
            return tickets;
        }
        sqlite3_bind_text(stmt, 1, customerName.c_str(), -1, SQLITE_TRANSIENT);
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
            std::cerr << "Failed to prepare statement: " << sqlite3_errmsg(db) << std::endl;
            return;
        }
        sqlite3_bind_int(stmt, 1, ticketId);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::cerr << "Failed to execute delete: " << sqlite3_errmsg(db) << std::endl;
        }
        sqlite3_finalize(stmt);
    }

    void close() {
        if (db) {
            sqlite3_close(db);
            db = nullptr;
        }
    }
};