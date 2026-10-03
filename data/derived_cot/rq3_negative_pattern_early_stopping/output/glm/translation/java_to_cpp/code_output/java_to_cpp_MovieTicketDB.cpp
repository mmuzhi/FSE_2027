// MovieTicketDB.cpp
#include "MovieTicketDB.h"

MovieTicketDB::MovieTicketDB(const std::string& dbName) : connection(nullptr) {
    int rc = sqlite3_open(dbName.c_str(), &connection);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << sqlite3_errmsg(connection) << std::endl;
        sqlite3_close(connection);
        connection = nullptr;
        return;
    }
    createTable();
}

MovieTicketDB::~MovieTicketDB() {
    close();
}

void MovieTicketDB::createTable() {
    const char* sql = "CREATE TABLE IF NOT EXISTS tickets ("
                      "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                      "movie_name TEXT, "
                      "theater_name TEXT, "
                      "seat_number TEXT, "
                      "customer_name TEXT)";
    char* errMsg = nullptr;
    int rc = sqlite3_exec(connection, sql, nullptr, nullptr, &errMsg);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << errMsg << std::endl;
        sqlite3_free(errMsg);
    }
}

void MovieTicketDB::insertTicket(const std::string& movieName, const std::string& theaterName,
                                  const std::string& seatNumber, const std::string& customerName) {
    const char* sql = "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) VALUES (?, ?, ?, ?)";
    sqlite3_stmt* stmt = nullptr;
    int rc = sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << sqlite3_errmsg(connection) << std::endl;
        return;
    }
    sqlite3_bind_text(stmt, 1, movieName.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 2, theaterName.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 3, seatNumber.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 4, customerName.c_str(), -1, SQLITE_TRANSIENT);

    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        std::cerr << "SQL error: " << sqlite3_errmsg(connection) << std::endl;
    }
    sqlite3_finalize(stmt);
}

std::vector<MovieTicketDB::Ticket> MovieTicketDB::searchTicketsByCustomer(const std::string& customerName) {
    const char* sql = "SELECT * FROM tickets WHERE customer_name = ?";
    std::vector<Ticket> tickets;
    sqlite3_stmt* stmt = nullptr;
    int rc = sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << sqlite3_errmsg(connection) << std::endl;
        return tickets;
    }
    sqlite3_bind_text(stmt, 1, customerName.c_str(), -1, SQLITE_TRANSIENT);

    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        int id = sqlite3_column_int(stmt, 0);
        const char* movieNamePtr = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        const char* theaterNamePtr = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 2));
        const char* seatNumberPtr = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3));
        const char* customerNamePtr = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));
        std::string movieNameVal = movieNamePtr ? movieNamePtr : "";
        std::string theaterNameVal = theaterNamePtr ? theaterNamePtr : "";
        std::string seatNumberVal = seatNumberPtr ? seatNumberPtr : "";
        std::string customerNameVal = customerNamePtr ? customerNamePtr : "";
        tickets.emplace_back(id, movieNameVal, theaterNameVal, seatNumberVal, customerNameVal);
    }

    if (rc != SQLITE_DONE) {
        std::cerr << "SQL error: " << sqlite3_errmsg(connection) << std::endl;
    }
    sqlite3_finalize(stmt);
    return tickets;
}

void MovieTicketDB::deleteTicket(int ticketId) {
    const char* sql = "DELETE FROM tickets WHERE id = ?";
    sqlite3_stmt* stmt = nullptr;
    int rc = sqlite3_prepare_v2(connection, sql, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << sqlite3_errmsg(connection) << std::endl;
        return;
    }
    sqlite3_bind_int(stmt, 1, ticketId);

    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        std::cerr << "SQL error: " << sqlite3_errmsg(connection) << std::endl;
    }
    sqlite3_finalize(stmt);
}

void MovieTicketDB::close() {
    if (connection != nullptr) {
        sqlite3_close(connection);
        connection = nullptr;
    }
}