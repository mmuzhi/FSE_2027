// org.example.DatabaseProcessor — C++ translation backed by the SQLite C API.
// Note: the Java static block loading "org.sqlite.JDBC" corresponds to linking
// against the SQLite library itself; there is no runtime driver registration.

#include <sqlite3.h>

#include <cstdint>
#include <iostream>
#include <map>
#include <optional>
#include <string>
#include <variant>
#include <vector>

namespace org::example {

// Java "Object" values used here are Integer, String, or null.
using Object = std::variant<std::monostate, int32_t, std::string>;
using Row = std::map<std::string, Object>;

class DatabaseProcessor {
private:
    std::string databaseName;

    static std::string objectToString(const Object& value) {
        // Mirrors Java String.format("%s", obj): null renders as "null",
        // Integer renders as its decimal digits, String as itself.
        if (const auto* s = std::get_if<std::string>(&value)) return *s;
        if (const auto* i = std::get_if<int32_t>(&value)) return std::to_string(*i);
        return "null";
    }

    static void printSQLException(const std::string& message) {
        // SQLException.printStackTrace() writes to stderr and swallows the error.
        std::cerr << "java.sql.SQLException: " << message << std::endl;
    }

    sqlite3* openConnection() const {
        sqlite3* conn = nullptr;
        if (sqlite3_open(databaseName.c_str(), &conn) != SQLITE_OK) {
            printSQLException(conn ? sqlite3_errmsg(conn) : "unable to open database");
            if (conn) sqlite3_close(conn);
            return nullptr;
        }
        return conn;
    }

    void executeStatement(sqlite3* conn, const std::string& sql) const {
        char* errMsg = nullptr;
        if (sqlite3_exec(conn, sql.c_str(), nullptr, nullptr, &errMsg) != SQLITE_OK) {
            printSQLException(errMsg ? errMsg : sqlite3_errmsg(conn));
        }
        if (errMsg) sqlite3_free(errMsg);
    }

    static int columnIndex(sqlite3_stmt* stmt, const char* name) {
        const int count = sqlite3_column_count(stmt);
        for (int i = 0; i < count; ++i) {
            if (std::string(sqlite3_column_name(stmt, i)) == name) return i;
        }
        return -1;
    }

public:
    explicit DatabaseProcessor(std::string dbName)
        : databaseName(std::move(dbName)) {}

    void createTable(const std::string& tableName,
                     const std::string& key1,
                     const std::string& key2) const {
        sqlite3* conn = openConnection();
        if (!conn) return;
        const std::string createTableQuery =
            "CREATE TABLE IF NOT EXISTS " + tableName +
            " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " + key2 + " INTEGER)";
        executeStatement(conn, createTableQuery);
        sqlite3_close(conn);
    }

    void insertIntoDatabase(const std::string& tableName,
                            const std::vector<Row>& data) const {
        sqlite3* conn = openConnection();
        if (!conn) return;
        for (const auto& item : data) {
            // Java: item.get("name") -> null renders as "null" inside the quotes;
            // item.get("age") -> null causes an uncaught NullPointerException.
            const std::string nameValue =
                item.count("name") ? objectToString(item.at("name")) : "null";
            const int32_t ageValue =
                std::get<int32_t>(item.at("age")); // throws if missing/wrong type (NPE/CCE analog)

            const std::string insertQuery =
                "INSERT INTO " + tableName + " (name, age) VALUES ('" +
                nameValue + "', " + std::to_string(ageValue) + ")";
            executeStatement(conn, insertQuery);
        }
        sqlite3_close(conn);
    }

    std::optional<std::vector<Row>> searchDatabase(const std::string& tableName,
                                                   const std::string& name) const {
        std::vector<Row> result;
        sqlite3* conn = openConnection();
        if (conn) {
            const std::string selectQuery =
                "SELECT * FROM " + tableName + " WHERE name = '" + name + "'";
            sqlite3_stmt* stmt = nullptr;
            if (sqlite3_prepare_v2(conn, selectQuery.c_str(), -1, &stmt, nullptr) == SQLITE_OK) {
                while (sqlite3_step(stmt) == SQLITE_ROW) {
                    Row row;
                    const int idIdx = columnIndex(stmt, "id");
                    const int nameIdx = columnIndex(stmt, "name");
                    const int ageIdx = columnIndex(stmt, "age");
                    if (idIdx >= 0)
                        row["id"] = static_cast<int32_t>(sqlite3_column_int(stmt, idIdx));
                    if (nameIdx >= 0) {
                        const unsigned char* text = sqlite3_column_text(stmt, nameIdx);
                        row["name"] = text
                            ? Object{std::in_place_type<std::string>,
                                     reinterpret_cast<const char*>(text)}
                            : Object{std::monostate{}}; // SQL NULL -> Java null
                    }
                    if (ageIdx >= 0)
                        row["age"] = static_cast<int32_t>(sqlite3_column_int(stmt, ageIdx));
                    result.push_back(std::move(row));
                }
            } else {
                printSQLException(sqlite3_errmsg(conn));
            }
            if (stmt) sqlite3_finalize(stmt);
            sqlite3_close(conn);
        }
        return result.empty() ? std::nullopt : std::optional<std::vector<Row>>{std::move(result)};
    }

    void deleteFromDatabase(const std::string& tableName, const std::string& name) const {
        sqlite3* conn = openConnection();
        if (!conn) return;
        const std::string deleteQuery =
            "DELETE FROM " + tableName + " WHERE name = '" + name + "'";
        executeStatement(conn, deleteQuery);
        sqlite3_close(conn);
    }
};

} // namespace org::example