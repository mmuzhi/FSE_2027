#include <sqlite3.h>
#include <string>
#include <vector>
#include <tuple>
#include <optional>
#include <stdexcept>

class DatabaseProcessor {
public:
    std::string database_name;

    DatabaseProcessor(const std::string& database_name) : database_name(database_name) {}

    void create_table(const std::string& table_name, const std::string& key1, const std::string& key2) {
        sqlite3* db;
        if (sqlite3_open(database_name.c_str(), &db) != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error(err);
        }

        std::string query = "CREATE TABLE IF NOT EXISTS " + table_name +
            " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " + key2 + " INTEGER)";

        char* errmsg = nullptr;
        if (sqlite3_exec(db, query.c_str(), nullptr, nullptr, &errmsg) != SQLITE_OK) {
            std::string err(errmsg);
            sqlite3_free(errmsg);
            sqlite3_close(db);
            throw std::runtime_error(err);
        }

        sqlite3_close(db);
    }

    void insert_into_database(const std::string& table_name,
                               const std::vector<std::pair<std::string, int>>& data) {
        sqlite3* db;
        if (sqlite3_open(database_name.c_str(), &db) != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error(err);
        }

        std::string query = "INSERT INTO " + table_name + " (name, age) VALUES (?, ?)";

        sqlite3_stmt* stmt;
        if (sqlite3_prepare_v2(db, query.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error(err);
        }

        for (const auto& item : data) {
            sqlite3_bind_text(stmt, 1, item.first.c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_bind_int(stmt, 2, item.second);

            if (sqlite3_step(stmt) != SQLITE_DONE) {
                std::string err = sqlite3_errmsg(db);
                sqlite3_finalize(stmt);
                sqlite3_close(db);
                throw std::runtime_error(err);
            }
            sqlite3_reset(stmt);
            sqlite3_clear_bindings(stmt);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);
    }

    std::optional<std::vector<std::tuple<int, std::string, int>>>
    search_database(const std::string& table_name, const std::string& name) {
        sqlite3* db;
        if (sqlite3_open(database_name.c_str(), &db) != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error(err);
        }

        std::string query = "SELECT * FROM " + table_name + " WHERE name = ?";

        sqlite3_stmt* stmt;
        if (sqlite3_prepare_v2(db, query.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error(err);
        }

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);

        std::vector<std::tuple<int, std::string, int>> results;

        while (sqlite3_step(stmt) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            std::string name_val = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            int age = sqlite3_column_int(stmt, 2);
            results.emplace_back(id, name_val, age);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);

        if (results.empty()) {
            return std::nullopt;
        }
        return results;
    }

    void delete_from_database(const std::string& table_name, const std::string& name) {
        sqlite3* db;
        if (sqlite3_open(database_name.c_str(), &db) != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error(err);
        }

        std::string query = "DELETE FROM " + table_name + " WHERE name = ?";

        sqlite3_stmt* stmt;
        if (sqlite3_prepare_v2(db, query.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error(err);
        }

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_finalize(stmt);
            sqlite3_close(db);
            throw std::runtime_error(err);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);
    }
};