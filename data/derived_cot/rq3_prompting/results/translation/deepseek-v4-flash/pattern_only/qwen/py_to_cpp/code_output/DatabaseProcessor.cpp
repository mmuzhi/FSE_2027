#include <sqlite3.h>
#include <string>
#include <vector>
#include <map>
#include <variant>
#include <optional>
#include <stdexcept>
#include <cstdint>
#include <utility>

class DatabaseProcessor {
public:
    using SqlValue = std::variant<std::monostate, int, double, std::string, std::vector<uint8_t>>;
    using Row = std::vector<SqlValue>;
    using DataItem = std::map<std::string, SqlValue>;

    explicit DatabaseProcessor(const std::string& database_name)
        : database_name_(database_name) {}

    void create_table(const std::string& table_name, const std::string& key1, const std::string& key2) {
        SQLiteDB db(database_name_);
        std::string query = "CREATE TABLE IF NOT EXISTS " + table_name +
                            " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " + key2 + " INTEGER)";
        exec_sql(db.get(), query, "Failed to create table");
    }

    void insert_into_database(const std::string& table_name, const std::vector<DataItem>& data) {
        SQLiteDB db(database_name_);
        exec_sql(db.get(), "BEGIN", "Failed to begin transaction");
        try {
            std::string query = "INSERT INTO " + table_name + " (name, age) VALUES (?, ?)";
            for (const auto& item : data) {
                auto name_it = item.find("name");
                if (name_it == item.end()) throw std::out_of_range("name");
                auto age_it = item.find("age");
                if (age_it == item.end()) throw std::out_of_range("age");

                sqlite3_stmt* stmt = nullptr;
                int rc = sqlite3_prepare_v2(db.get(), query.c_str(), -1, &stmt, nullptr);
                if (rc != SQLITE_OK) {
                    throw std::runtime_error("Failed to prepare insert: " + std::string(sqlite3_errmsg(db.get())));
                }
                bind_sql_value(stmt, 1, name_it->second);
                bind_sql_value(stmt, 2, age_it->second);
                rc = sqlite3_step(stmt);
                sqlite3_finalize(stmt);
                if (rc != SQLITE_DONE) {
                    throw std::runtime_error("Failed to execute insert: " + std::string(sqlite3_errmsg(db.get())));
                }
            }
            exec_sql(db.get(), "COMMIT", "Failed to commit transaction");
        } catch (...) {
            sqlite3_exec(db.get(), "ROLLBACK", nullptr, nullptr, nullptr);
            throw;
        }
    }

    std::optional<std::vector<Row>> search_database(const std::string& table_name, const std::string& name) {
        SQLiteDB db(database_name_);
        std::string query = "SELECT * FROM " + table_name + " WHERE name = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db.get(), query.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error("Failed to prepare select: " + std::string(sqlite3_errmsg(db.get())));
        }
        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);

        std::vector<Row> rows;
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            int cols = sqlite3_column_count(stmt);
            Row row;
            row.reserve(cols);
            for (int i = 0; i < cols; ++i) {
                row.push_back(column_to_value(stmt, i));
            }
            rows.push_back(std::move(row));
        }
        sqlite3_finalize(stmt);

        if (rc != SQLITE_DONE) {
            throw std::runtime_error("Failed to execute select: " + std::string(sqlite3_errmsg(db.get())));
        }
        if (rows.empty()) {
            return std::nullopt;
        }
        return rows;
    }

    void delete_from_database(const std::string& table_name, const std::string& name) {
        SQLiteDB db(database_name_);
        exec_sql(db.get(), "BEGIN", "Failed to begin transaction");
        try {
            std::string query = "DELETE FROM " + table_name + " WHERE name = ?";
            sqlite3_stmt* stmt = nullptr;
            int rc = sqlite3_prepare_v2(db.get(), query.c_str(), -1, &stmt, nullptr);
            if (rc != SQLITE_OK) {
                throw std::runtime_error("Failed to prepare delete: " + std::string(sqlite3_errmsg(db.get())));
            }
            sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);
            rc = sqlite3_step(stmt);
            sqlite3_finalize(stmt);
            if (rc != SQLITE_DONE) {
                throw std::runtime_error("Failed to execute delete: " + std::string(sqlite3_errmsg(db.get())));
            }
            exec_sql(db.get(), "COMMIT", "Failed to commit transaction");
        } catch (...) {
            sqlite3_exec(db.get(), "ROLLBACK", nullptr, nullptr, nullptr);
            throw;
        }
    }

private:
    class SQLiteDB {
    public:
        explicit SQLiteDB(const std::string& path) {
            int rc = sqlite3_open(path.c_str(), &db_);
            if (rc != SQLITE_OK) {
                std::string msg = db_ ? sqlite3_errmsg(db_) : "unknown error";
                if (db_) sqlite3_close(db_);
                db_ = nullptr;
                throw std::runtime_error("Failed to open database: " + msg);
            }
        }
        ~SQLiteDB() {
            if (db_) sqlite3_close(db_);
        }
        sqlite3* get() const { return db_; }
        SQLiteDB(const SQLiteDB&) = delete;
        SQLiteDB& operator=(const SQLiteDB&) = delete;
    private:
        sqlite3* db_ = nullptr;
    };

    static void exec_sql(sqlite3* db, const std::string& sql, const std::string& error_context) {
        char* errMsg = nullptr;
        int rc = sqlite3_exec(db, sql.c_str(), nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::string msg = errMsg ? errMsg : "unknown error";
            sqlite3_free(errMsg);
            throw std::runtime_error(error_context + ": " + msg);
        }
    }

    static void bind_sql_value(sqlite3_stmt* stmt, int idx, const SqlValue& val) {
        if (std::holds_alternative<std::monostate>(val)) {
            sqlite3_bind_null(stmt, idx);
        } else if (auto p = std::get_if<int>(&val)) {
            sqlite3_bind_int(stmt, idx, *p);
        } else if (auto p = std::get_if<double>(&val)) {
            sqlite3_bind_double(stmt, idx, *p);
        } else if (auto p = std::get_if<std::string>(&val)) {
            sqlite3_bind_text(stmt, idx, p->c_str(), -1, SQLITE_TRANSIENT);
        } else if (auto p = std::get_if<std::vector<uint8_t>>(&val)) {
            sqlite3_bind_blob(stmt, idx, p->data(), static_cast<int>(p->size()), SQLITE_TRANSIENT);
        }
    }

    static SqlValue column_to_value(sqlite3_stmt* stmt, int col) {
        int type = sqlite3_column_type(stmt, col);
        switch (type) {
            case SQLITE_INTEGER:
                return sqlite3_column_int(stmt, col);
            case SQLITE_FLOAT:
                return sqlite3_column_double(stmt, col);
            case SQLITE_TEXT: {
                const unsigned char* text = sqlite3_column_text(stmt, col);
                int size = sqlite3_column_bytes(stmt, col);
                return std::string(reinterpret_cast<const char*>(text), size);
            }
            case SQLITE_BLOB: {
                const void* data = sqlite3_column_blob(stmt, col);
                int size = sqlite3_column_bytes(stmt, col);
                if (size > 0) {
                    const uint8_t* bytes = static_cast<const uint8_t*>(data);
                    return std::vector<uint8_t>(bytes, bytes + size);
                } else {
                    return std::vector<uint8_t>();
                }
            }
            case SQLITE_NULL:
            default:
                return std::monostate{};
        }
    }

    std::string database_name_;
};