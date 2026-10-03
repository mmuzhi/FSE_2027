#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <sqlite3.h>
#include <stdexcept>
#include <memory>

class StudentDatabaseProcessor {
private:
    std::string databaseName;

    sqlite3* getConnection() {
        sqlite3* db;
        int rc = sqlite3_open(databaseName.c_str(), &db);
        if (rc != SQLITE_OK) {
            std::cerr << "Can't open database: " << sqlite3_errmsg(db) << std::endl;
            sqlite3_close(db);
            return nullptr;
        }
        return db;
    }

    void closeConnection(sqlite3* db) {
        if (db) {
            sqlite3_close(db);
        }
    }

public:
    class StudentData {
    private:
        std::string name;
        int age;
        std::string gender;
        int grade;

    public:
        StudentData(const std::string& name, int age, const std::string& gender, int grade)
            : name(name), age(age), gender(gender), grade(grade) {}

        const std::string& getName() const { return name; }
        int getAge() const { return age; }
        const std::string& getGender() const { return gender; }
        int getGrade() const { return grade; }
    };

    StudentDatabaseProcessor(const std::string& databaseName) : databaseName(databaseName) {}

    void createStudentTable() {
        sqlite3* db = getConnection();
        if (!db) return;
        const char* createTableQuery =
            "CREATE TABLE IF NOT EXISTS students ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT, "
            "age INTEGER, "
            "gender TEXT, "
            "grade INTEGER"
            ")";
        char* errMsg = nullptr;
        int rc = sqlite3_exec(db, createTableQuery, nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::cerr << "SQL error: " << errMsg << std::endl;
            sqlite3_free(errMsg);
        }
        closeConnection(db);
    }

    void insertStudent(const StudentData& studentData) {
        sqlite3* db = getConnection();
        if (!db) return;
        const char* insertQuery = "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)";
        sqlite3_stmt* stmt;
        int rc = sqlite3_prepare_v2(db, insertQuery, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << "SQL error: " << sqlite3_errmsg(db) << std::endl;
            closeConnection(db);
            return;
        }
        sqlite3_bind_text(stmt, 1, studentData.getName().c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_int(stmt, 2, studentData.getAge());
        sqlite3_bind_text(stmt, 3, studentData.getGender().c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_int(stmt, 4, studentData.getGrade());
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::cerr << "Execution error: " << sqlite3_errmsg(db) << std::endl;
        }
        sqlite3_finalize(stmt);
        closeConnection(db);
    }

    std::vector<std::map<std::string, std::string>> searchStudentByName(const std::string& name) {
        sqlite3* db = getConnection();
        std::vector<std::map<std::string, std::string>> result;
        if (!db) return result;
        const char* selectQuery = "SELECT * FROM students WHERE name = ?";
        sqlite3_stmt* stmt;
        int rc = sqlite3_prepare_v2(db, selectQuery, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << "SQL error: " << sqlite3_errmsg(db) << std::endl;
            closeConnection(db);
            return result;
        }
        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            std::map<std::string, std::string> student;
            student["id"] = std::to_string(sqlite3_column_int(stmt, 0));
            student["name"] = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
            student["age"] = std::to_string(sqlite3_column_int(stmt, 2));
            student["gender"] = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 3));
            student["grade"] = std::to_string(sqlite3_column_int(stmt, 4));
            result.push_back(student);
        }
        if (rc != SQLITE_DONE) {
            std::cerr << "Execution error: " << sqlite3_errmsg(db) << std::endl;
        }
        sqlite3_finalize(stmt);
        closeConnection(db);
        return result;
    }

    void deleteStudentByName(const std::string& name) {
        sqlite3* db = getConnection();
        if (!db) return;
        const char* deleteQuery = "DELETE FROM students WHERE name = ?";
        sqlite3_stmt* stmt;
        int rc = sqlite3_prepare_v2(db, deleteQuery, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            std::cerr << "SQL error: " << sqlite3_errmsg(db) << std::endl;
            closeConnection(db);
            return;
        }
        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);
        rc = sqlite3_step(stmt);
        if (rc != SQLITE_DONE) {
            std::cerr << "Execution error: " << sqlite3_errmsg(db) << std::endl;
        }
        sqlite3_finalize(stmt);
        closeConnection(db);
    }
};