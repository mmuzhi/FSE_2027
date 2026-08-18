#include <sqlite3.h>

#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <tuple>
#include <variant>
#include <vector>

// Translation of the Python DatabaseProcessor. Links against the sqlite3 C API.
// Notes on behavioral fidelity:
// - Each method opens/closes its own connection, exactly like sqlite3.connect()/close().
// - create_table builds the exact same (malformed) SQL string, so it fails with the
//   same error the Python version raises (sqlite3.OperationalError -> std::runtime_error).
// - insert/delete run inside an explicit BEGIN/COMMIT so that a failure mid-loop
//   rolls back (connection close discards the open transaction), matching Python's
//   commit-on-success / rollback-on-error behavior.
// - search_database returns nullopt where Python returns None.

class DatabaseProcessor {
public:
    // A data row: {'name': <string>, 'age': <int>} (variant mirrors mixed dict values).
    using Value = std::variant<std::string, int>;
    using Row = std::map<std::string, Value>;
    // Each result row: (id, name, age); nullopt represents Python's None.
    using SearchResult = std::optional<std::vector<std::tuple<int, std::string, int>>>;

    std::string database_name;

    explicit DatabaseProcessor(std::string database_name_)
        : database_name(std::move(database_name_)) {}

    void create_table(const std::string& table_name,
                      const std::string& /*key1*/,
                      const std::string& /*key2*/) {
        sqlite3* conn = open_connection();
        Guard guard{conn, nullptr};

        const std::string create_table_query =
            "CREATE TABLE IF NOT EXISTS " + table_name +
            " (id INTEGER PRIMARY KEY, 7af79e972756839df6c048825a40129b.t2YijyRWHfaS6qEp TEXT,  INTEGER)";

        if (sqlite3_prepare_v2(conn, create_table_query.c_str(), -1, &guard.stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(conn));
        }
        if (sqlite3_step(guard.stmt) != SQLITE_DONE) {
            throw std::runtime_error(sqlite3_errmsg(conn));
        }
    }

    void insert_into_database(const std::string& table_name, const std::vector<Row>& data) {
        sqlite3* conn = open_connection();
        Guard guard{conn, nullptr};

        const std::string insert_query =
            "INSERT INTO " + table_name + " (name, age) VALUES (?, ?)";
        if (sqlite3_prepare_v2(conn, insert_query.c_str(), -1, &guard.stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(conn));
        }

        char* err = nullptr;
        if (sqlite3_exec(conn, "BEGIN;", nullptr, nullptr, &err) != SQLITE_OK) {
            std::string msg = err ? err : sqlite3_errmsg(conn);
            sqlite3_free(err);
            throw std::runtime_error(msg);
        }

        for (const Row& item : data) {
            sqlite3_reset(guard.stmt);
            sqlite3_clear_bindings(guard.stmt);

            // item['name'] / item['age']: at() throws (like KeyError) if missing.
            bind_value(guard.stmt, 1, item.at("name"));
            bind_value(guard.stmt, 2, item.at("age"));

            if (sqlite3_step(guard.stmt) != SQLITE_DONE) {
                throw std::runtime_error(sqlite3_errmsg(conn));
            }
        }

        // conn.commit()
        if (sqlite3_exec(conn, "COMMIT;", nullptr, nullptr, &err) != SQLITE_OK) {
            std::string msg = err ? err : sqlite3_errmsg(conn);
            sqlite3_free(err);
            throw std::runtime_error(msg);
        }
    }

    SearchResult search_database(const std::string& table_name, const std::string& name) {
        sqlite3* conn = open_connection();
        Guard guard{conn, nullptr};

        const std::string select_query =
            "SELECT * FROM " + table_name + " WHERE name = ?";
        if (sqlite3_prepare_v2(conn, select_query.c_str(), -1, &guard.stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(conn));
        }
        sqlite3_bind_text(guard.stmt, 1, name.c_str(),
                          static_cast<int>(name.size()), SQLITE_TRANSIENT);

        std::vector<std::tuple<int, std::string, int>> result;
        int rc;
        while ((rc = sqlite3_step(guard.stmt)) == SQLITE_ROW) {
            const unsigned char* text = sqlite3_column_text(guard.stmt, 1);
            result.emplace_back(
                sqlite3_column_int(guard.stmt, 0),
                text ? std::string(reinterpret_cast<const char*>(text)) : std::string(),
                sqlite3_column_int(guard.stmt, 2));
        }
        if (rc != SQLITE_DONE) {
            throw std::runtime_error(sqlite3_errmsg(conn));
        }

        if (!result.empty()) {
            return result;
        }
        return std::nullopt;
    }

    void delete_from_database(const std::string& table_name, const std::string& name) {
        sqlite3* conn = open_connection();
        Guard guard{conn, nullptr};

        const std::string delete_query =
            "DELETE FROM " + table_name + " WHERE name = ?";
        if (sqlite3_prepare_v2(conn, delete_query.c_str(), -1, &guard.stmt, nullptr) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(conn));
        }
        sqlite3_bind_text(guard.stmt, 1, name.c_str(),
                          static_cast<int>(name.size()), SQLITE_TRANSIENT);

        if (sqlite3_step(guard.stmt) != SQLITE_DONE) {
            throw std::runtime_error(sqlite3_errmsg(conn));
        }
    }

private:
    struct Guard {
        sqlite3* conn;
        sqlite3_stmt* stmt;
        ~Guard() {
            if (stmt) sqlite3_finalize(stmt);
            if (conn) sqlite3_close(conn);  // discards any open transaction (rollback)
        }
    };

    sqlite3* open_connection() const {
        sqlite3* conn = nullptr;
        if (sqlite3_open(database_name.c_str(), &conn) != SQLITE_OK) {
            std::string msg = conn ? sqlite3_errmsg(conn) : "unable to open database file";
            if (conn) sqlite3_close(conn);
            throw std::runtime_error(msg);
        }
        return conn;
    }

    static void bind_value(sqlite3_stmt* stmt, int idx, const Value& value) {
        if (const std::string* s = std::get_if<std::string>(&value)) {
            sqlite3_bind_text(stmt, idx, s->c_str(),
                              static_cast<int>(s->size()), SQLITE_TRANSIENT);
        } else {
            sqlite3_bind_int(stmt, idx, std::get<int>(value));
        }
    }
};