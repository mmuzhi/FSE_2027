#include <sqlite3.h>

#include <iostream>
#include <string>
#include <vector>

namespace org {
namespace example {

class MovieTicketDB {
private:
    sqlite3* connection;

    void printSQLException() {
        std::cerr << "java.sql.SQLException: "
                  << (connection ? sqlite3_errmsg(connection) : "unknown error")
                  << std::endl;
    }

    void createTable() {
        const char* sql =
                "CREATE TABLE IF NOT EXISTS tickets ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "movie_name TEXT, "
                "theater_name TEXT, "
                "seat_number TEXT, "
                "customer_name TEXT)";
        char* errMsg = nullptr;
        if (sqlite3_exec(connection, sql, nullptr, nullptr, &errMsg) != SQLITE_OK) {
            std::cerr << "java.sql.SQLException: "
                      << (errMsg ? errMsg : "unknown error") << std::endl;
            sqlite3_free(errMsg);
        }
    }

public:
    class Ticket {
    public:
        Ticket(int id, std::string movieName, std::string theaterName,
               std::string seatNumber, std::string customerName)
            : id(id),
              movieName(std::move(movieName)),
              theaterName(std::move(theaterName)),
              seatNumber(std::move(seatNumber)),
              customerName(std::move(customerName)) {}

        int getId() const { return id; }
        const std::string& getMovieName() const { return movieName; }
        const std::string& getTheaterName() const { return theaterName; }
        const std::string& getSeatNumber() const { return seatNumber; }
        const std::string& getCustomerName() const { return customerName; }

    private:
        int id;
        std::string movieName;
        std::string theaterName;
        std::string seatNumber;
        std::string customerName;
    };

    explicit MovieTicketDB(const std::string& dbName) : connection(nullptr) {
        if (sqlite3_open(dbName.c_str(), &connection) == SQLITE_OK) {
            createTable();
        } else {
            std::cerr << "java.sql.SQLException: "
                      << sqlite3_errmsg(connection) << std::endl;
            sqlite3_close(connection);
            connection = nullptr;
        }
    }

    MovieTicketDB(const MovieTicketDB&) = delete;
    MovieTicketDB& operator=(const MovieTicketDB&) = delete;

    ~MovieTicketDB() { close(); }

    void insertTicket(const std::string& movieName, const std::string& theaterName,
                      const std::string& seatNumber, const std::string& customerName) {
        const char* sql = "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) VALUES (?, ?, ?, ?)";
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &pstmt, nullptr) != SQLITE_OK) {
            printSQLException();
            return;
        }
        sqlite3_bind_text(pstmt, 1, movieName.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(pstmt, 2, theaterName.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(pstmt, 3, seatNumber.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(pstmt, 4, customerName.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(pstmt) != SQLITE_DONE) {
            printSQLException();
        }
        sqlite3_finalize(pstmt);
    }

    std::vector<Ticket> searchTicketsByCustomer(const std::string& customerName) {
        const char* sql = "SELECT * FROM tickets WHERE customer_name = ?";
        std::vector<Ticket> tickets;
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &pstmt, nullptr) != SQLITE_OK) {
            printSQLException();
            return tickets;
        }
        sqlite3_bind_text(pstmt, 1, customerName.c_str(), -1, SQLITE_TRANSIENT);

        auto columnText = [](sqlite3_stmt* stmt, int col) -> std::string {
            const unsigned char* text = sqlite3_column_text(stmt, col);
            return text ? reinterpret_cast<const char*>(text) : "";
        };

        int rc = sqlite3_step(pstmt);
        while (rc == SQLITE_ROW) {
            tickets.emplace_back(
                sqlite3_column_int(pstmt, 0),
                columnText(pstmt, 1),
                columnText(pstmt, 2),
                columnText(pstmt, 3),
                columnText(pstmt, 4));
            rc = sqlite3_step(pstmt);
        }
        if (rc != SQLITE_DONE) {
            printSQLException();
        }
        sqlite3_finalize(pstmt);
        return tickets;
    }

    void deleteTicket(int ticketId) {
        const char* sql = "DELETE FROM tickets WHERE id = ?";
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &pstmt, nullptr) != SQLITE_OK) {
            printSQLException();
            return;
        }
        sqlite3_bind_int(pstmt, 1, ticketId);
        if (sqlite3_step(pstmt) != SQLITE_DONE) {
            printSQLException();
        }
        sqlite3_finalize(pstmt);
    }

    void close() {
        if (connection != nullptr) {
            sqlite3_close(connection);
            connection = nullptr;
        }
    }
};

}  // namespace example
}  // namespace org