#include <iostream>
#include <vector>
#include <map>
#include <memory>
#include <sqlite3.h>

// RAII wrapper for SQLite connection
class SQLiteConnection {
public:
    explicit SQLiteConnection(const char* filename) : db(nullptr) {
        int rc = sqlite3_open(filename, &db);
        if (rc != SQLITE_OK) {
            // Print error and leave db as nullptr
            std::cerr << "Error opening database: " << sqlite3_errmsg(db) << std::endl;
        }
    }

    ~SQLiteConnection() {
        if (db != nullptr) {
            sqlite3_close(db);
        }
    }

    sqlite3* get() const { return db; }

private:
    sqlite3* db;
};

// RAII wrapper for SQLite statement
class SQLiteStatement {
public:
    SQLiteStatement(SQLiteConnection& conn, const char* sql) : conn(conn), stmt(nullptr) {
        int rc = sqlite3_prepare_v2(conn.get(), sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << "Failed to prepare statement: " << sqlite3_errmsg(conn.get()) << std::endl;
        }
    }

    ~SQLiteStatement() {
        if (stmt != nullptr) {
            sqlite3_finalize(stmt);
        }
    }

    bool execute() {
        return sqlite3_step(stmt) == SQLITE_DONE;
    }

    bool next() {
        return sqlite3_step(stmt) == SQLITE_ROW;
    }

    int getInt(const char* columnName, int index) {
        return sqlite3_column_int(stmt, index);
    }

    const unsigned char* getString(const char* columnName, int index) {
        return sqlite3_column_text(stmt, index);
    }

    // We don't expose the raw stmt pointer

private:
    SQLiteConnection& conn;
    sqlite3_stmt* stmt;
};

// RAII wrapper for SQLite result set (actually, we can reuse SQLiteStatement for both execute and query)
// But note: the original code uses Statement for both execute and executeQuery. We can use the same wrapper.

class DatabaseProcessor {
public:
    DatabaseProcessor(const std::string& databaseName) : dbName(databaseName) {}

    void createTable(const std::string& tableName, const std::string& key1, const std::string& key2) {
        std::string createTableQuery = 
            "CREATE TABLE IF NOT EXISTS " + tableName + " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " + key2 + " INTEGER)";

        try (SQLiteConnection conn(dbName.c_str());
             SQLiteStatement stmt(conn, createTableQuery.c_str())) {
            stmt.execute();
        } catch (...) {
            // We don't throw exceptions, we print and continue (like the original Java code)
            // But note: the original Java code catches SQLException and prints. We do the same.
            std::cerr << "Error creating table." << std::endl;
        }
    }

    void insertIntoDatabase(const std::string& tableName, const std::vector<std::map<std::string, int>>& data) {
        // Note: The original Java code expects a List<Map<String, Object>>, but we are using a vector of maps with int for age.
        // We'll assume the age is integer. If the original code uses Object, we can use variant or dynamic type, but to keep behavior identical, we use int.

        // However, the original code uses String.format with %d for age. We assume integer.

        try (SQLiteConnection conn(dbName.c_str())) {
            for (const auto& item : data) {
                // We assume the map has "name" and "age"
                std::string name = item.at("name");
                int age = item.at("age");

                std::string insertQuery = 
                    "INSERT INTO " + tableName + " (name, age) VALUES ('" + name + "', " + std::to_string(age) + ")";

                SQLiteStatement stmt(conn, insertQuery.c_str());
                stmt.execute();
            }
        } catch (...) {
            std::cerr << "Error inserting data." << std::endl;
        }
    }

    std::vector<std::map<std::string, int>> searchDatabase(const std::string& tableName, const std::string& name) {
        std::vector<std::map<std::string, int>> result;

        try (SQLiteConnection conn(dbName.c_str())) {
            std::string selectQuery = "SELECT * FROM " + tableName + " WHERE name = '" + name + "'";
            SQLiteStatement stmt(conn, selectQuery.c_str());

            // Check if the statement executed successfully
            if (stmt.next()) {
                // We are going to loop until there are no more rows
                while (true) {
                    std::map<std::string, int> row;
                    row["id"] = stmt.getInt("id", 0);
                    row["name"] = reinterpret_cast<const std::string&>(stmt.getString("name", 0));
                    row["age"] = stmt.getInt("age", 2); // Assuming columns: id, name, age (so age is at index 2)

                    result.push_back(row);

                    if (!stmt.next()) {
                        break;
                    }
                }
            }
        } catch (...) {
            std::cerr << "Error searching database." << std::endl;
        }

        return result.empty() ? nullptr : result;
    }

    void deleteFromDatabase(const std::string& tableName, const std::string& name) {
        std::string deleteQuery = "DELETE FROM " + tableName + " WHERE name = '" + name + "'";

        try (SQLiteConnection conn(dbName.c_str())) {
            SQLiteStatement stmt(conn, deleteQuery.c_str());
            stmt.execute();
        } catch (...) {
            std::cerr << "Error deleting data." << std::endl;
        }
    }

private:
    std::string dbName;
};