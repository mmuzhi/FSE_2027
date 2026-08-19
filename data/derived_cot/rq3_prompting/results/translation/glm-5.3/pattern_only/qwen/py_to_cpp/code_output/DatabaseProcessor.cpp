#include <sqlite3.h>

#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <tuple>
#include <type_traits>
#include <variant>
#include <vector>

class DatabaseProcessor {
public:
    using DbValue = std::variant<std::string, int>;   // value of a dict entry
    using Row = std::map<std::string, DbValue>;       // one dict {name, age}
    using ResultRow = std::tuple<int, std::string, int>;  // (id, name, age)

    explicit DatabaseProcessor(const std::string& database_name)
        : database_name(database_name) {}

    // Create a new table in the database if it doesn't exist.
    // key1/key2 are accepted but unused, exactly as in the original.
    void create_table(const std::string& table_name,
                      const std::string& key1,
                      const std::string& key2) {
        (void)key1;
        (void)key2;
        sqlite3* conn = open_connection();

        std::string create_table_query =
            "CREATE TABLE IF NOT EXISTS " + table_name +
            " (id INTEGER PRIMARY KEY, 7af79e972756839df6c048825a40129b.t2YijyRWHfaS6qEp TEXT,  INTEGER)";
        execute(conn, create_table_query);

        sqlite3_close(conn);
    }

    void insert_into_database(const std::string& table_name,
                              const std::vector<Row>& data) {
        sqlite3* conn = open_connection();

        for (const auto& item : data) {
            std::string insert_query =
                "INSERT INTO " + table_name + " (name, age) VALUES (?, ?)";
            sqlite3_stmt* stmt = prepare(conn, insert_query);

            // .at() throws std::out_of_range like Python's KeyError on item['name']
            bind_value(stmt, 1, item.at("name"));
            bind_value(stmt, 2, item.at("age"));

            if (sqlite3_step(stmt) != SQLITE_DONE) {
                std::string msg = sqlite3_errmsg(conn);
                sqlite3_finalize(stmt);
                sqlite3_close(conn);
                throw std::runtime_error(msg);
            }
            sqlite3_finalize(stmt);
        }

        // statements run in autocommit mode -> committed on close,
        // matching conn.commit(); conn.close()
        sqlite3_close(conn);
    }

    std::optional<std::vector<ResultRow>>
    search_database(const std::string& table_name, const std::string& name) {
        sqlite3* conn = open_connection();

        std::string select_query =
            "SELECT * FROM " + table_name + " WHERE name = ?";
        sqlite3_stmt* stmt = prepare(conn, select_query);
        bind_value(stmt, 1, name);

        std::vector<ResultRow> result;
        int rc;
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            const unsigned char* text = sqlite3_column_text(stmt, 1);
            result.emplace_back(
                static_cast<int>(sqlite3_column_int(stmt, 0)),
                text ? std::string(reinterpret_cast<const char*>(text))
                     : std::string(),
                static_cast<int>(sqlite3_column_int(stmt, 2)));
        }
        if (rc != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(conn);
            sqlite3_finalize(stmt);
            sqlite3_close(conn);
            throw std::runtime_error(msg);
        }
        sqlite3_finalize(stmt);
        sqlite3_close(conn);

        if (!result.empty()) {
            return result;   // non-empty list of rows
        }
        return std::nullopt; // None when nothing matched
    }

    void delete_from_database(const std::string& table_name,
                              const std::string& name) {
        sqlite3* conn = open_connection();

        std::string delete_query =
            "DELETE FROM " + table_name + " WHERE name = ?";
        sqlite3_stmt* stmt = prepare(conn, delete_query);
        bind_value(stmt, 1, name);

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(conn);
            sqlite3_finalize(stmt);
            sqlite3_close(conn);
            throw std::runtime_error(msg);
        }
        sqlite3_finalize(stmt);

        // autocommit -> commit + close like conn.commit(); conn.close()
        sqlite3_close(conn);
    }

private:
    std::string database_name;

    sqlite3* open_connection() {
        sqlite3* conn = nullptr;
        if (sqlite3_open(database_name.c_str(), &conn) != SQLITE_OK) {
            std::string msg = conn ? sqlite3_errmsg(conn)
                                   : std::string("out of memory");
            if (conn) sqlite3_close(conn);
            throw std::runtime_error("unable to open database file: " + msg);
        }
        return conn;
    }

    void execute(sqlite3* conn, const std::string& sql) {
        char* err = nullptr;
        if (sqlite3_exec(conn, sql.c_str(), nullptr, nullptr, &err) != SQLITE_OK) {
            std::string msg = err ? std::string(err) : sqlite3_errmsg(conn);
            sqlite3_free(err);
            sqlite3_close(conn);
            throw std::runtime_error(msg);  // mirrors sqlite3.OperationalError
        }
        sqlite3_free(err);
    }

    sqlite3_stmt* prepare(sqlite3* conn, const std::string& sql) {
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(conn, sql.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
            std::string msg = sqlite3_errmsg(conn);
            if (stmt) sqlite3_finalize(stmt);
            sqlite3_close(conn);
            throw std::runtime_error(msg);
        }
        return stmt;
    }

    static void bind_value(sqlite3_stmt* stmt, int index, const DbValue& value) {
        std::visit([&](const auto& v) {
            using T = std::decay_t<decltype(v)>;
            int rc;
            if constexpr (std::is_same_v<T, int>) {
                rc = sqlite3_bind_int(stmt, index, v);
            } else {
                rc = sqlite3_bind_text(stmt, index, v.c_str(), -1,
                                       SQLITE_TRANSIENT);
            }
            if (rc != SQLITE_OK) {
                throw std::runtime_error("parameter binding failed");
            }
        }, value);
    }
};