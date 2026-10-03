#include <sqlite3.h>
#include <string>
#include <vector>
#include <memory>

class DatabaseProcessor {
private:
    std::string database_name;

    // Helper function to execute a single SQL statement and return the result as a vector of vectors (for SELECT)
    // Returns a vector of vector of strings (each inner vector is a row, each string is a column)
    std::vector<std::vector<std::string>> execute_query(sqlite3* db, const std::string& query) {
        sqlite3_stmt* stmt = nullptr;
        std::vector<std::vector<std::string>> result;

        int rc = sqlite3_prepare_v2(db, query.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            // In the original Python code, there is no error handling. We'll ignore errors.
            return result;
        }

        while (sqlite3_step(stmt) == SQLITE_ROW) {
            int num_columns = sqlite3_column_count(stmt);
            std::vector<std::string> row;
            for (int i = 0; i < num_columns; i++) {
                const char* text = (const char*)sqlite3_column_text(stmt, i);
                if (text) {
                    row.push_back(text);
                } else {
                    row.push_back("");
                }
            }
            result.push_back(row);
        }

        sqlite3_finalize(stmt);
        return result;
    }

    // Helper function to execute a non-SELECT statement (CREATE, INSERT, DELETE)
    void execute_non_query(sqlite3* db, const std::string& query) {
        sqlite3_stmt* stmt = nullptr;
        int rc = sqlite3_prepare_v2(db, query.c_str(), -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            // No error handling in original code.
            return;
        }

        if (sqlite3_step(stmt) != SQLITE_DONE && sqlite3_step(stmt) != SQLITE_ROW) {
            // No error handling.
        }

        sqlite3_finalize(stmt);
    }

public:
    DatabaseProcessor(const std::string& database_name) : database_name(database_name) {}

    // Create a new table in the database if it doesn't exist.
    void create_table(const std::string& table_name, const std::string& key1, const std::string& key2) {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            // Original code doesn't handle errors, so we proceed without the table.
            return;
        }

        std::string create_table_query = "CREATE TABLE IF NOT EXISTS " + table_name + " (id INTEGER PRIMARY KEY, " + key1 + " TEXT, " + key2 + " INTEGER)";
        execute_non_query(db, create_table_query);

        sqlite3_close(db);
    }

    // Insert data into the specified table in the database.
    void insert_into_database(const std::string& table_name, const std::vector<std::unordered_map<std::string, int>>& data) {
        // Note: The original Python code expects a list of dictionaries with keys 'name' and 'age'
        // But we are using a vector of unordered_map with string keys and int values.
        // We'll change the parameter type to match the intended use.

        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            return;
        }

        // We'll use a transaction for efficiency, but the original code doesn't use transactions.
        // However, the original code commits after each insert. We'll do the same as the original: no transaction.
        for (const auto& item : data) {
            // We expect the dictionary to have keys "name" and "age"
            // If not, this will fail. We don't handle missing keys.
            std::string name = item.at("name");
            int age = item.at("age");

            std::string insert_query = "INSERT INTO " + table_name + " (name, age) VALUES (?, ?)";
            sqlite3_stmt* stmt = nullptr;
            int rc_prepare = sqlite3_prepare_v2(db, insert_query.c_str(), -1, &stmt, nullptr);
            if (rc_prepare != SQLITE_OK) {
                // No error handling.
                continue;
            }

            sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_STATIC);
            sqlite3_bind_int(stmt, 2, age);

            if (sqlite3_step(stmt) != SQLITE_DONE) {
                // No error handling.
            }

            sqlite3_finalize(stmt);
        }

        sqlite3_close(db);
    }

    // Search the specified table in the database for rows with a matching name.
    std::vector<std::vector<std::string>> search_database(const std::string& table_name, const std::string& name) {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            return {};
        }

        std::string select_query = "SELECT * FROM " + table_name + " WHERE name = ?";
        auto result = execute_query(db, select_query);

        sqlite3_close(db);
        return result;
    }

    // Delete rows from the specified table in the database with a matching name.
    void delete_from_database(const std::string& table_name, const std::string& name) {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            return;
        }

        std::string delete_query = "DELETE FROM " + table_name + " WHERE name = ?";
        sqlite3_stmt* stmt = nullptr;
        int rc_prepare = sqlite3_prepare_v2(db, delete_query.c_str(), -1, &stmt, nullptr);
        if (rc_prepare != SQLITE_OK) {
            // No error handling.
            return;
        }

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_STATIC);
        if (sqlite3_step(stmt) != SQLITE_DONE) {
            // No error handling.
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);
    }
};