#include <sqlite3.h>
#include <iostream>
#include <string>
#include <vector>
#include <optional>
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
        int rc = sqlite3_exec(db, sql, nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            if (errMsg != nullptr) {
                std::cerr << errMsg << std::endl;
                sqlite3_free(errMsg);
            } else {
                std::cerr << sqlite3_errmsg(db) << std::endl;
            }
        }
    }

    int bindOptionalText(sqlite3_stmt* stmt, int index, const std::optional<std::string>& value) {
        if (value.has_value()) {
            return sqlite3_bind_text(stmt, index, value->c_str(), -1, SQLITE_TRANSIENT);
        } else {
            return sqlite3_bind_null(stmt, index);
        }
    }

    std::optional<std::string> getOptionalString(sqlite3_stmt* stmt, int col) {
        const unsigned char* text = sqlite3_column_text(stmt, col);
        if (text == nullptr) {
            return std::nullopt;
        }
        return std::string(reinterpret_cast<const char*>(text));
    }

public:
    MovieTicketDB(const std::string& dbName) : db(nullptr) {
        int rc = sqlite3_open(dbName.c_str(), &db);
        if (rc != SQLITE_OK) {
            if (db != nullptr) {
                std::cerr << sqlite3_errmsg(db) << std::endl;
                sqlite3_close(db);
                db = nullptr;
            } else {
                std::cerr << "sqlite3_open failed" << std::endl;
            }
        } else {
            createTable();
        }
    }

    void insertTicket(const std::optional<std::string>& movieName,
                      const std::optional<std::string>& theaterName,
                      const std::optional<std::string>& seatNumber,
                      const std::optional<std::string>& customerName) {
        if (db == nullptr) throw std::runtime_error("NullPointerException");
        const char* sql = "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) VALUES (?, ?, ?, ?)";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(db) << std::endl;
            return;
        }

        rc = bindOptionalText(stmt, 1, movieName);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(db) << std::endl;
            sqlite3_finalize(stmt);
            return;
        }
        rc = bindOptionalText(stmt, 2, theaterName);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(db) << std::endl;
            sqlite3_finalize(stmt);
            return;
        }
        rc = bindOptionalText(stmt, 3, seatNumber);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(db) << std::endl;
            sqlite3_finalize(stmt);
            return;
        }
        rc = bindOptionalText(stmt, 4, customerName);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(db) << std::endl;
            sqlite3_finalize(stmt);
            return;
        }

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::cerr << sqlite3_errmsg(db) << std::endl;
        }
        sqlite3_finalize(stmt);
    }

    std::vector<Ticket> searchTicketsByCustomer(const std::optional<std::string>& customerName) {
        if (db == nullptr) throw std::runtime_error("NullPointerException");
        std::vector<Ticket> tickets;
        const char* sql = "SELECT * FROM tickets WHERE customer_name = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(db) << std::endl;
            return tickets;
        }

        rc = bindOptionalText(stmt, 1, customerName);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(db) << std::endl;
            sqlite3_finalize(stmt);
            return tickets;
        }

        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            std::optional<std::string> movieName = getOptionalString(stmt, 1);
            std::optional<std::string> theaterName = getOptionalString(stmt, 2);
            std::optional<std::string> seatNumber = getOptionalString(stmt, 3);
            std::optional<std::string> customer = getOptionalString(stmt, 4);
            tickets.emplace_back(id, movieName, theaterName, seatNumber, customer);
        }

        if (rc != SQLITE_DONE) {
            std::cerr << sqlite3_errmsg(db) << std::endl;
        }
        sqlite3_finalize(stmt);
        return tickets;
    }

    void deleteTicket(int ticketId) {
        if (db == nullptr) throw std::runtime_error("NullPointerException");
        const char* sql = "DELETE FROM tickets WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(db) << std::endl;
            return;
        }

        rc = sqlite3_bind_int(stmt, 1, ticketId);
        if (rc != SQLITE_OK) {
            std::cerr << sqlite3_errmsg(db) << std::endl;
            sqlite3_finalize(stmt);
            return;
        }

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::cerr << sqlite3_errmsg(db) << std::endl;
        }
        sqlite3_finalize(stmt);
    }

    void close() {
        if (db != nullptr) {
            int rc = sqlite3_close(db);
            if (rc != SQLITE_OK) {
                std::cerr << sqlite3_errmsg(db) << std::endl;
            } else {
                db = nullptr;
            }
        }
    }

    class Ticket {
    private:
        int id;
        std::optional<std::string> movieName;
        std::optional<std::string> theaterName;
        std::optional<std::string> seatNumber;
        std::optional<std::string> customerName;

    public:
        Ticket(int id,
               const std::optional<std::string>& movieName,
               const std::optional<std::string>& theaterName,
               const std::optional<std::string>& seatNumber,
               const std::optional<std::string>& customerName)
            : id(id), movieName(movieName), theaterName(theaterName), seatNumber(seatNumber), customerName(customerName) {}

        int getId() const { return id; }
        std::optional<std::string> getMovieName() const { return movieName; }
        std::optional<std::string> getTheaterName() const { return theaterName; }
        std::optional<std::string> getSeatNumber() const { return seatNumber; }
        std::optional<std::string> getCustomerName() const { return customerName; }
    };
};