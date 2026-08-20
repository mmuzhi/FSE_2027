#include <cstdio>
#include <string>
#include <vector>

#include <sqlite3.h>

namespace org {
namespace example {

class MovieTicketDB {
public:
    // Equivalent of Java's nested "public static class Ticket"
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
        // DriverManager.getConnection("jdbc:sqlite:" + dbName)
        if (sqlite3_open(dbName.c_str(), &connection) != SQLITE_OK) {
            printSQLException("sqlite3_open");
            if (connection != nullptr) {
                sqlite3_close(connection);
                connection = nullptr;
            }
            return;
        }
        createTable();
    }

    // Java has no destructor; this ensures cleanup and does not change observable behavior
    ~MovieTicketDB() {
        close();
    }

    MovieTicketDB(const MovieTicketDB&) = delete;
    MovieTicketDB& operator=(const MovieTicketDB&) = delete;

    void insertTicket(const std::string& movieName, const std::string& theaterName,
                      const std::string& seatNumber, const std::string& customerName) {
        const char* sql =
            "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) VALUES (?, ?, ?, ?)";
        sqlite3_stmt* stmt = nullptr;
        if (!connectionUsable() ||
            sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            printSQLException("sqlite3_prepare_v2");
            return;
        }
        sqlite3_bind_text(stmt, 1, movieName.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, theaterName.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, seatNumber.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 4, customerName.c_str(), -1, SQLITE_TRANSIENT);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            printSQLException("sqlite3_step");
        }
        sqlite3_finalize(stmt);
    }

    std::vector<Ticket> searchTicketsByCustomer(const std::string& customerName) {
        const char* sql = "SELECT * FROM tickets WHERE customer_name = ?";
        std::vector<Ticket> tickets;
        sqlite3_stmt* stmt = nullptr;
        if (!connectionUsable() ||
            sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            printSQLException("sqlite3_prepare_v2");
            return tickets;
        }
        sqlite3_bind_text(stmt, 1, customerName.c_str(), -1, SQLITE_TRANSIENT);
        int rc;
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            tickets.emplace_back(
                sqlite3_column_int(stmt, 0),
                columnText(stmt, 1),
                columnText(stmt, 2),
                columnText(stmt, 3),
                columnText(stmt, 4));
        }
        if (rc != SQLITE_DONE) {
            printSQLException("sqlite3_step");
        }
        sqlite3_finalize(stmt);
        return tickets;
    }

    void deleteTicket(int ticketId) {
        const char* sql = "DELETE FROM tickets WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        if (!connectionUsable() ||
            sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            printSQLException("sqlite3_prepare_v2");
            return;
        }
        sqlite3_bind_int(stmt, 1, ticketId);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            printSQLException("sqlite3_step");
        }
        sqlite3_finalize(stmt);
    }

    void close() {
        // Equivalent of: if (connection != null && !connection.isClosed()) connection.close();
        if (connection != nullptr) {
            sqlite3_close(connection);
            connection = nullptr;
        }
    }

private:
    sqlite3* connection;

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
            std::fprintf(stderr, "java.sql.SQLException: %s\n",
                         errMsg != nullptr ? errMsg : "unknown error");
            if (errMsg != nullptr) {
                sqlite3_free(errMsg);
            }
        }
    }

    bool connectionUsable() const {
        return connection != nullptr;
    }

    // Mirrors catch (SQLException e) { e.printStackTrace(); } which writes to stderr
    void printSQLException(const char* operation) const {
        const char* msg =
            (connection != nullptr) ? sqlite3_errmsg(connection) : "no connection available";
        std::fprintf(stderr, "java.sql.SQLException: %s (%s)\n", msg, operation);
    }

    static std::string columnText(sqlite3_stmt* stmt, int index) {
        const unsigned char* text = sqlite3_column_text(stmt, index);
        return (text != nullptr) ? std::string(reinterpret_cast<const char*>(text))
                                 : std::string();
    }
};

} // namespace example
} // namespace org