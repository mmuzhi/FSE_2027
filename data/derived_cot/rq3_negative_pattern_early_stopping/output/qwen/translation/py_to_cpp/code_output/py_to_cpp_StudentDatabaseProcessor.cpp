#include <sqlite3.h>
#include <string>
#include <map>
#include <vector>
#include <stdexcept>
#include <tuple>

class KeyError : public std::exception {
public:
    std::string key;
    KeyError(const std::string& key) : key(key) {}
    const char* what() const noexcept override {
        return ("Key not found: " + key).c_str();
    }
};

class DatabaseError : public std::exception {
public:
    std::string message;
    DatabaseError(const std::string& msg) : message(msg) {}
    const char* what() const noexcept override {
        return message.c_str();
    }
};

class StudentDatabaseProcessor {
private:
    std::string database_name;

public:
    StudentDatabaseProcessor(const std::string& database_name) : database_name(database_name) {}

    void create_student_table() {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            throw DatabaseError("Cannot open database: " + std::string(sqlite3_errmsg(db)));
        }

        const char* create_table_query = R"(CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            grade INTEGER
        ))";
        char* error_msg = nullptr;
        rc = sqlite3_exec(db, create_table_query, nullptr, nullptr, &error_msg);
        if (rc != SQLITE_OK) {
            sqlite3_free(error_msg);
            throw DatabaseError("Failed to create table: " + std::string(error_msg));
        }

        sqlite3_close(db);
    }

    void insert_student(const std::map<std::string, std::string>& student_data) {
        // Validate required keys
        if (student_data.find("name") == student_data.end() ||
            student_data.find("age") == student_data.end() ||
            student_data.find("gender") == student_data.end() ||
            student_data.find("grade") == student_data.end()) {
            throw KeyError("Missing required keys in student data");
        }

        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            throw DatabaseError("Cannot open database: " + std::string(sqlite3_errmsg(db)));
        }

        const char* insert_query = "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)";
        sqlite3_stmt* stmt = nullptr;
        rc = sqlite3_prepare_v2(db, insert_query, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            sqlite3_close(db);
            throw DatabaseError("Failed to prepare insert statement: " + std::string(sqlite3_errmsg(db)));
        }

        try {
            sqlite3_bind_text(stmt, 1, student_data["name"].c_str(), -1, SQLITE_STATIC);
            sqlite3_bind_text(stmt, 2, student_data["age"].c_str(), -1, SQLITE_STATIC);
            sqlite3_bind_text(stmt, 3, student_data["gender"].c_str(), -1, SQLITE_STATIC);
            sqlite3_bind_text(stmt, 4, student_data["grade"].c_str(), -1, SQLITE_STATIC);

            rc = sqlite3_step(stmt);
            if (rc != SQLITE_DONE) {
                const char* error_msg = sqlite3_errmsg(db);
                sqlite3_finalize(stmt);
                sqlite3_close(db);
                throw DatabaseError("Failed to insert student: " + std::string(error_msg));
            }
        } catch (...) {
            sqlite3_finalize(stmt);
            sqlite3_close(db);
            throw;
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);
    }

    std::vector<std::tuple<int, std::string, int, std::string, int>> search_student_by_name(const std::string& name) {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            throw DatabaseError("Cannot open database: " + std::string(sqlite3_errmsg(db)));
        }

        const char* select_query = "SELECT * FROM students WHERE name = ?";
        sqlite3_stmt* stmt = nullptr;
        rc = sqlite3_prepare_v2(db, select_query, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            sqlite3_close(db);
            throw DatabaseError("Failed to prepare select statement: " + std::string(sqlite3_errmsg(db)));
        }

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_STATIC);
        rc = sqlite3_step(stmt);
        std::vector<std::tuple<int, std::string, int, std::string, int>> result;
        while (rc == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const char* name_str = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            int age = sqlite3_column_int(stmt, 2);
            const char* gender_str = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3));
            int grade = sqlite3_column_int(stmt, 4);
            result.push_back(std::make_tuple(id, name_str, age, gender_str, grade));
            rc = sqlite3_step(stmt);
        }

        if (rc != SQLITE_DONE) {
            const char* error_msg = sqlite3_errmsg(db);
            sqlite3_finalize(stmt);
            sqlite3_close(db);
            throw DatabaseError("Failed to execute select statement: " + std::string(error_msg));
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return result;
    }

    void delete_student_by_name(const std::string& name) {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            throw DatabaseError("Cannot open database: " + std::string(sqlite3_errmsg(db)));
        }

        const char* delete_query = "DELETE FROM students WHERE name = ?";
        sqlite3_stmt* stmt = nullptr;
        rc = sqlite3_prepare_v2(db, delete_query, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            sqlite3_close(db);
            throw DatabaseError("Failed to prepare delete statement: " + std::string(sqlite3_errmsg(db)));
        }

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_STATIC);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            const char* error_msg = sqlite3_errmsg(db);
            sqlite3_finalize(stmt);
            sqlite3_close(db);
            throw DatabaseError("Failed to delete student: " + std::string(error_msg));
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);
    }
};