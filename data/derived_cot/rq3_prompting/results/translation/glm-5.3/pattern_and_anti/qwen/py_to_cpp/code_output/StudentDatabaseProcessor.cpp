#include <sqlite3.h>

#include <map>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

// Mirrors the Python StudentDatabaseProcessor: each operation opens the
// SQLite database, executes one statement, commits implicitly, and closes.
// Errors surface as exceptions, analogous to sqlite3 raising in Python.
class StudentDatabaseProcessor {
public:
    // Analog of the Python dict parameter (keys: "name", "age", "gender", "grade").
    // Numeric strings bound into INTEGER-affinity columns are stored as
    // integers, matching the Python behavior of binding ints.
    using StudentData = std::map<std::string, std::string>;
    // Analog of Python's list of row tuples: (id, name, age, gender, grade).
    using Row = std::tuple<int, std::string, int, std::string, int>;

    explicit StudentDatabaseProcessor(std::string database_name)
        : database_name_(std::move(database_name)) {}

    void create_student_table() {
        sqlite3* db = open_database();

        const char* create_table_query =
            "CREATE TABLE IF NOT EXISTS students ("
            "id INTEGER PRIMARY KEY, "
            "name TEXT, "
            "age INTEGER, "
            "gender TEXT, "
            "grade INTEGER"
            ")";

        char* err_msg = nullptr;
        if (sqlite3_exec(db, create_table_query, nullptr, nullptr, &err_msg) != SQLITE_OK) {
            std::string msg = err_msg ? err_msg : sqlite3_errmsg(db);
            sqlite3_free(err_msg);
            sqlite3_close(db);
            throw std::runtime_error(msg);  // analog of sqlite3.OperationalError
        }

        sqlite3_close(db);
    }

    void insert_student(const StudentData& student_data) {
        sqlite3* db = open_database();

        sqlite3_stmt* stmt = nullptr;
        const char* insert_query =
            "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)";
        if (sqlite3_prepare_v2(db, insert_query, -1, &stmt, nullptr) != SQLITE_OK) {
            std::string msg = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error(msg);
        }

        // .at() throws on a missing key, mirroring Python's KeyError.
        bind_text(stmt, 1, student_data.at("name"));
        bind_text(stmt, 2, student_data.at("age"));
        bind_text(stmt, 3, student_data.at("gender"));
        bind_text(stmt, 4, student_data.at("grade"));

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(db);
            sqlite3_finalize(stmt);
            sqlite3_close(db);
            throw std::runtime_error(msg);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);  // closing commits (autocommit mode), as in Python
    }

    std::vector<Row> search_student_by_name(const std::string& name) {
        sqlite3* db = open_database();

        sqlite3_stmt* stmt = nullptr;
        const char* select_query = "SELECT * FROM students WHERE name = ?";
        if (sqlite3_prepare_v2(db, select_query, -1, &stmt, nullptr) != SQLITE_OK) {
            std::string msg = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error(msg);
        }

        bind_text(stmt, 1, name);

        std::vector<Row> result;
        int rc = sqlite3_step(stmt);
        while (rc == SQLITE_ROW) {
            result.emplace_back(
                sqlite3_column_int(stmt, 0),
                column_text(stmt, 1),
                sqlite3_column_int(stmt, 2),
                column_text(stmt, 3),
                sqlite3_column_int(stmt, 4));
            rc = sqlite3_step(stmt);
        }
        if (rc != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(db);
            sqlite3_finalize(stmt);
            sqlite3_close(db);
            throw std::runtime_error(msg);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);

        return result;
    }

    void delete_student_by_name(const std::string& name) {
        sqlite3* db = open_database();

        sqlite3_stmt* stmt = nullptr;
        const char* delete_query = "DELETE FROM students WHERE name = ?";
        if (sqlite3_prepare_v2(db, delete_query, -1, &stmt, nullptr) != SQLITE_OK) {
            std::string msg = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error(msg);
        }

        bind_text(stmt, 1, name);

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(db);
            sqlite3_finalize(stmt);
            sqlite3_close(db);
            throw std::runtime_error(msg);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);
    }

private:
    std::string database_name_;

    sqlite3* open_database() const {
        sqlite3* db = nullptr;
        if (sqlite3_open(database_name_.c_str(), &db) != SQLITE_OK) {
            std::string msg = db ? sqlite3_errmsg(db) : "unable to open database file";
            if (db) sqlite3_close(db);
            throw std::runtime_error(msg);
        }
        return db;
    }

    static void bind_text(sqlite3_stmt* stmt, int index, const std::string& value) {
        if (sqlite3_bind_text(stmt, index, value.c_str(), -1, SQLITE_TRANSIENT) != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(sqlite3_db_handle(stmt)));
        }
    }

    static std::string column_text(sqlite3_stmt* stmt, int index) {
        const unsigned char* text = sqlite3_column_text(stmt, index);
        return text ? std::string(reinterpret_cast<const char*>(text)) : std::string();
    }
};