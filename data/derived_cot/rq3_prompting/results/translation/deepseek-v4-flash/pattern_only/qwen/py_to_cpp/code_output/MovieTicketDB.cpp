#include <sqlite3.h>
#include <string>
#include <vector>
#include <tuple>
#include <stdexcept>

class MovieTicketDB {
public:
    MovieTicketDB(const std::string& db_name) {
        int rc = sqlite3_open(db_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errstr(rc);
            if (db) sqlite3_close(db);
            throw std::runtime_error("Cannot open database: " + err);
        }
        try {
            create_table();
        } catch (...) {
            sqlite3_close(db);
            throw;
        }
    }

    ~MovieTicketDB() {
        if (db) sqlite3_close(db);
    }

    MovieTicketDB(const MovieTicketDB&) = delete;
    MovieTicketDB& operator=(const MovieTicketDB&) = delete;

    void create_table() {
        const char* sql = "CREATE TABLE IF NOT EXISTS tickets ("
                          "id INTEGER PRIMARY KEY, "
                          "movie_name TEXT, "
                          "theater_name TEXT, "
                          "seat_number TEXT, "
                          "customer_name TEXT)";
        char* errmsg = nullptr;
        int rc = sqlite3_exec(db, sql, nullptr, nullptr, &errmsg);
        if (rc != SQLITE_OK) {
            std::string err = errmsg ? errmsg : "unknown error";
            sqlite3_free(errmsg);
            throw std::runtime_error("create_table failed: " + err);
        }
    }

    void insert_ticket(const std::string& movie_name, const std::string& theater_name,
                       const std::string& seat_number, const std::string& customer_name) {
        const char* sql = "INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name) VALUES (?, ?, ?, ?)";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("prepare insert failed: " + std::string(sqlite3_errmsg(db)));
        }

        auto bind_text = [&](int idx, const std::string& val) {
            int b_rc = sqlite3_bind_text(stmt, idx, val.c_str(), static_cast<int>(val.size()), SQLITE_TRANSIENT);
            if (b_rc != SQLITE_OK) {
                sqlite3_finalize(stmt);
                throw std::runtime_error("bind text failed: " + std::string(sqlite3_errmsg(db)));
            }
        };

        bind_text(1, movie_name);
        bind_text(2, theater_name);
        bind_text(3, seat_number);
        bind_text(4, customer_name);

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_finalize(stmt);
            throw std::runtime_error("insert_ticket failed: " + err);
        }
        sqlite3_finalize(stmt);
    }

    std::vector<std::tuple<int, std::string, std::string, std::string, std::string>>
    search_tickets_by_customer(const std::string& customer_name) {
        const char* sql = "SELECT * FROM tickets WHERE customer_name = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("prepare search failed: " + std::string(sqlite3_errmsg(db)));
        }

        int b_rc = sqlite3_bind_text(stmt, 1, customer_name.c_str(), static_cast<int>(customer_name.size()), SQLITE_TRANSIENT);
        if (b_rc != SQLITE_OK) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("bind search failed: " + std::string(sqlite3_errmsg(db)));
        }

        std::vector<std::tuple<int, std::string, std::string, std::string, std::string>> results;
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const unsigned char* movie = sqlite3_column_text(stmt, 1);
            const unsigned char* theater = sqlite3_column_text(stmt, 2);
            const unsigned char* seat = sqlite3_column_text(stmt, 3);
            const unsigned char* customer = sqlite3_column_text(stmt, 4);

            int movie_len = sqlite3_column_bytes(stmt, 1);
            int theater_len = sqlite3_column_bytes(stmt, 2);
            int seat_len = sqlite3_column_bytes(stmt, 3);
            int customer_len = sqlite3_column_bytes(stmt, 4);

            results.emplace_back(
                id,
                movie ? std::string(reinterpret_cast<const char*>(movie), movie_len) : std::string(),
                theater ? std::string(reinterpret_cast<const char*>(theater), theater_len) : std::string(),
                seat ? std::string(reinterpret_cast<const char*>(seat), seat_len) : std::string(),
                customer ? std::string(reinterpret_cast<const char*>(customer), customer_len) : std::string()
            );
        }

        if (rc != SQLITE_DONE) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_finalize(stmt);
            throw std::runtime_error("search_tickets_by_customer failed: " + err);
        }
        sqlite3_finalize(stmt);
        return results;
    }

    void delete_ticket(int ticket_id) {
        const char* sql = "DELETE FROM tickets WHERE id = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("prepare delete failed: " + std::string(sqlite3_errmsg(db)));
        }

        int b_rc = sqlite3_bind_int(stmt, 1, ticket_id);
        if (b_rc != SQLITE_OK) {
            sqlite3_finalize(stmt);
            throw std::runtime_error("bind delete failed: " + std::string(sqlite3_errmsg(db)));
        }

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_finalize(stmt);
            throw std::runtime_error("delete_ticket failed: " + err);
        }
        sqlite3_finalize(stmt);
    }

private:
    sqlite3* db = nullptr;
};