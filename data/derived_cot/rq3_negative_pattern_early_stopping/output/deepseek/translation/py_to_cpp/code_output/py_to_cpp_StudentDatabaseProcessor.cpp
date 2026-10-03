#include <sqlite3.h>
#include <string>
#include <vector>
#include <stdexcept>
#include <cstring>

struct Student {
    int id;
    std::string name;
    int age;
    std::string gender;
    int grade;
};

class StudentDatabaseProcessor {
private:
    std::string database_name;

public:
    StudentDatabaseProcessor(const std::string& database_name)
        : database_name(database_name) {}

    void create_student_table() {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Cannot open database: " + err);
        }

        const char* create_table_sql =
            "CREATE TABLE IF NOT EXISTS students ("
            "id INTEGER PRIMARY KEY, "
            "name TEXT, "
            "age INTEGER, "
            "gender TEXT, "
            "grade INTEGER);";

        char* errmsg = nullptr;
        rc = sqlite3_exec(db, create_table_sql, nullptr, nullptr, &errmsg);
        if (rc != SQLITE_OK) {
            std::string err = errmsg;
            sqlite3_free(errmsg);
            sqlite3_close(db);
            throw std::runtime_error("SQL error: " + err);
        }

        sqlite3_close(db);
    }

    void insert_student(const Student& student) {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Cannot open database: " + err);
        }

        const char* insert_sql =
            "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?);";

        sqlite3_stmt* stmt = nullptr;
        rc = sqlite3_prepare_v2(db, insert_sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Prepare error: " + err);
        }

        sqlite3_bind_text(stmt, 1, student.name.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_int(stmt, 2, student.age);
        sqlite3_bind_text(stmt, 3, student.gender.c_str(), -1, SQLITE_STATIC);
        sqlite3_bind_int(stmt, 4, student.grade);

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_finalize(stmt);
            sqlite3_close(db);
            throw std::runtime_error("Insert error: " + err);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);
    }

    std::vector<Student> search_student_by_name(const std::string& name) {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Cannot open database: " + err);
        }

        const char* select_sql = "SELECT id, name, age, gender, grade FROM students WHERE name = ?;";

        sqlite3_stmt* stmt = nullptr;
        rc = sqlite3_prepare_v2(db, select_sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Prepare error: " + err);
        }

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_STATIC);

        std::vector<Student> results;
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            Student s;
            s.id = sqlite3_column_int(stmt, 0);
            const char* name_str = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            s.name = name_str ? name_str : "";
            s.age = sqlite3_column_int(stmt, 2);
            const char* gender_str = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3));
            s.gender = gender_str ? gender_str : "";
            s.grade = sqlite3_column_int(stmt, 4);
            results.push_back(s);
        }

        if (rc != SQLITE_DONE) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_finalize(stmt);
            sqlite3_close(db);
            throw std::runtime_error("Step error: " + err);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);
        return results;
    }

    void delete_student_by_name(const std::string& name) {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Cannot open database: " + err);
        }

        const char* delete_sql = "DELETE FROM students WHERE name = ?;";

        sqlite3_stmt* stmt = nullptr;
        rc = sqlite3_prepare_v2(db, delete_sql, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_close(db);
            throw std::runtime_error("Prepare error: " + err);
        }

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_STATIC);

        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::string err = sqlite3_errmsg(db);
            sqlite3_finalize(stmt);
            sqlite3_close(db);
            throw std::runtime_error("Delete error: " + err);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);
    }
};