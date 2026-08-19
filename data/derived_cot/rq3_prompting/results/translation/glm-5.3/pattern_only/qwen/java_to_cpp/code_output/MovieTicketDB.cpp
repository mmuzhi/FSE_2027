#include <sqlite3.h>

#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

namespace org {
namespace example {

class MovieTicketDB {
public:
    // Java public static nested class
    class Ticket {
    private:
        int id;
        std::string movieName;
        std::string theaterName;
        std::string seatNumber;
        std::string customerName;

    public:
        Ticket(int id, const std::string& movieName, const std::string& theaterName,
               const std::string& seatNumber, const std::string& customerName)
            : id(id), movieName(movieName), theaterName(theaterName),
              seatNumber(seatNumber), customerName(customerName) {}

        int getId() const { return id; }
        const std::string& getMovieName() const { return movieName; }
        const std::string& getTheaterName() const { return theaterName; }
        const std::string& getSeatNumber() const { return seatNumber; }
        const std::string& getCustomerName() const { return customerName; }
    };

private:
    sqlite3* connection;

    // Closest analog of e.printStackTrace(): diagnostic on stderr, execution continues.
    static void printSQLException(const char* message) {
        std::fprintf(stderr, "SQLException: %s\n", message);
    }

    // Equivalent of ResultSet.getXxx(String columnName)
    static int columnIndex(sqlite3_stmt* stmt, const char* name) {
        int count = sqlite3_column_count(stmt);
        for (int i = 0; i < count; ++i) {
            const char* col = sqlite3_column_name(stmt, i);
            if (col != nullptr && std::strcmp(col, name) == 0) {
                return i;
            }
        }
        return -1;
    }

    // getString(): NULL column mapped to empty string
    static std::string columnText(sqlite3_stmt* stmt, int index) {
        const unsigned char* text = sqlite3_column_text(stmt, index);
        return text != nullptr ? std::string(reinterpret_cast<const char*>(text)) : std::string();
    }

    void createTable() {
        if (connection == nullptr) {
            printSQLException("no connection available");
            return;
        }
        const char* sql =
            "CREATE TABLE IF NOT EXISTS tickets ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "movie_name TEXT, "
            "theater_name TEXT, "
            "seat_number TEXT, "
            "customer_name TEXT)";
        char* errMsg = nullptr;
        int rc = sqlite3_exec(connection, sql, nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            printSQLException(errMsg != nullptr ? errMsg : sqlite3_errmsg(connection));
        }
        if (errMsg != nullptr) {
            sqlite3_free(errMsg);
        }
    }

public:
    explicit MovieTicketDB(const std::string& dbName) : connection(nullptr) {
        int rc = sqlite3_open(dbName.c_str(), &connection);
        if (rc != SQLITE_OK) {
            printSQLException(connection != nullptr ? sqlite3_errmsg(connection)
                                                    : "unable to open database");
            if (connection != nullptr) {
                sqlite3_close(connection);
                connection = nullptr;
            }
            return; // Matches Java: createTable() is skipped when getConnection fails.
        }
        createTable();
    }

    // No destructor close: like Java, cleanup relies on the explicit close() call.

    void insertTicket(const std::string& movieName, const std::string& theaterName,
                      const std::string& seatNumber, const std::string& customerName) {
        const char* sql =
            "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) "
            "VALUES (?, ?, ?, ?)";
        if (connection == nullptr) {
            printSQLException("no connection available");
            return;
        }
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &pstmt, nullptr) != SQLITE_OK) {
            printSQLException(sqlite3_errmsg(connection));
            if (pstmt != nullptr) sqlite3_finalize(pstmt);
            return;
        }
        // SQLite parameters are 1-based, matching JDBC.
        if (sqlite3_bind_text(pstmt, 1, movieName.c_str(), -1, SQLITE_TRANSIENT) != SQLITE_OK ||
            sqlite3_bind_text(pstmt, 2, theaterName.c_str(), -1, SQLITE_TRANSIENT) != SQLITE_OK ||
            sqlite3_bind_text(pstmt, 3, seatNumber.c_str(), -1, SQLITE_TRANSIENT) != SQLITE_OK ||
            sqlite3_bind_text(pstmt, 4, customerName.c_str(), -1, SQLITE_TRANSIENT) != SQLITE_OK ||
            sqlite3_step(pstmt) != SQLITE_DONE) {
            printSQLException(sqlite3_errmsg(connection));
        }
        sqlite3_finalize(pstmt); // try-with-resources close
    }

    std::vector<Ticket> searchTicketsByCustomer(const std::string& customerName) {
        const char* sql = "SELECT * FROM tickets WHERE customer_name = ?";
        std::vector<Ticket> tickets;
        if (connection == nullptr) {
            printSQLException("no connection available");
            return tickets;
        }
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &pstmt, nullptr) != SQLITE_OK) {
            printSQLException(sqlite3_errmsg(connection));
            if (pstmt != nullptr) sqlite3_finalize(pstmt);
            return tickets;
        }
        if (sqlite3_bind_text(pstmt, 1, customerName.c_str(), -1, SQLITE_TRANSIENT) != SQLITE_OK) {
            printSQLException(sqlite3_errmsg(connection));
            sqlite3_finalize(pstmt);
            return tickets;
        }
        const int idIdx = columnIndex(pstmt, "id");
        const int movieIdx = columnIndex(pstmt, "movie_name");
        const int theaterIdx = columnIndex(pstmt, "theater_name");
        const int seatIdx = columnIndex(pstmt, "seat_number");
        const int customerIdx = columnIndex(pstmt, "customer_name");
        if (idIdx < 0 || movieIdx < 0 || theaterIdx < 0 || seatIdx < 0 || customerIdx < 0) {
            printSQLException("column not found");
            sqlite3_finalize(pstmt);
            return tickets;
        }
        int rc;
        while ((rc = sqlite3_step(pstmt)) == SQLITE_ROW) {
            tickets.emplace_back(
                sqlite3_column_int(pstmt, idIdx),
                columnText(pstmt, movieIdx),
                columnText(pstmt, theaterIdx),
                columnText(pstmt, seatIdx),
                columnText(pstmt, customerIdx));
        }
        if (rc != SQLITE_DONE) {
            printSQLException(sqlite3_errmsg(connection));
        }
        sqlite3_finalize(pstmt);
        return tickets;
    }

    void deleteTicket(int ticketId) {
        const char* sql = "DELETE FROM tickets WHERE id = ?";
        if (connection == nullptr) {
            printSQLException("no connection available");
            return;
        }
        sqlite3_stmt* pstmt = nullptr;
        if (sqlite3_prepare_v2(connection, sql, -1, &pstmt, nullptr) != SQLITE_OK) {
            printSQLException(sqlite3_errmsg(connection));
            if (pstmt != nullptr) sqlite3_finalize(pstmt);
            return;
        }
        if (sqlite3_bind_int(pstmt, 1, ticketId) != SQLITE_OK ||
            sqlite3_step(pstmt) != SQLITE_DONE) {
            printSQLException(sqlite3_errmsg(connection));
        }
        sqlite3_finalize(pstmt);
    }

    void close() {
        if (connection != nullptr) {
            if (sqlite3_close(connection) != SQLITE_OK) {
                printSQLException(sqlite3_errmsg(connection));
            } else {
                connection = nullptr;
            }
        }
    }
};

} // namespace example
} // namespace org