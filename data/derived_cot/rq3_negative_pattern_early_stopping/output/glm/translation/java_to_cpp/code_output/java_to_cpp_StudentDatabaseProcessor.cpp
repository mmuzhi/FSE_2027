#include <string>
#include <vector>
#include <map>
#include <any>
#include <iostream>
#include <stdexcept>
#include <sqlite3.h>

class StudentDatabaseProcessor {
private:
    std::string databaseName;

    sqlite3* getConnection() {
        sqlite3* db = nullptr;
        int rc = sqlite3_open(databaseName.c_str(), &db);
        if (rc != SQLITE_OK) {
            std::string msg = db ? sqlite3_errmsg(db) : "Failed to open database";
            if (db) sqlite3_close(db);
            throw std::runtime_error(msg);
        }
        return db;
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

    StudentDatabaseProcessor(const std::string& databaseName)
        : databaseName(databaseName) {}

    void createStudentTable() {
        const char* createTableQuery =
            "CREATE TABLE IF NOT EXISTS students ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT, "
            "age INTEGER, "
            "gender TEXT, "
            "grade INTEGER"
            ")";

        sqlite3* db = nullptr;
        try {
            db = getConnection();
            char* errMsg = nullptr;
            int rc = sqlite3_exec(db, createTableQuery, nullptr, nullptr, &errMsg);
            if (rc != SQLITE_OK) {
                std::cerr << errMsg << std::endl;
                sqlite3_free(errMsg);
            }
            sqlite3_close(db);
        } catch (const std::exception& e) {
            std::cerr << e.what() << std::endl;
            if (db) sqlite3_close(db);
        }
    }

    void insertStudent(const StudentData& studentData) {
        const char* insertQuery = "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)";

        sqlite3* db = nullptr;
        sqlite3_stmt* pstmt = nullptr;
        try {
            db = getConnection();
            int rc = sqlite3_prepare_v2(db, insertQuery, -1, &pstmt, nullptr);
            if (rc != SQLITE_OK) {
                std::cerr << sqlite3_errmsg(db) << std::endl;
                sqlite3_close(db);
                return;
            }

            sqlite3_bind_text(pstmt, 1, studentData.getName().c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_bind_int(pstmt, 2, studentData.getAge());
            sqlite3_bind_text(pstmt, 3, studentData.getGender().c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_bind_int(pstmt, 4, studentData.getGrade());

            rc = sqlite3_step(pstmt);
            if (rc != SQLITE_DONE) {
                std::cerr << sqlite3_errmsg(db) << std::endl;
            }

            sqlite3_finalize(pstmt);
            sqlite3_close(db);
        } catch (const std::exception& e) {
            std::cerr << e.what() << std::endl;
            if (pstmt) sqlite3_finalize(pstmt);
            if (db) sqlite3_close(db);
        }
    }

    std::vector<std::map<std::string, std::any>> searchStudentByName(const std::string& name) {
        const char* selectQuery = "SELECT * FROM students WHERE name = ?";
        std::vector<std::map<std::string, std::any>> result;

        sqlite3* db = nullptr;
        sqlite3_stmt* pstmt = nullptr;
        try {
            db = getConnection();
            int rc = sqlite3_prepare_v2(db, selectQuery, -1, &pstmt, nullptr);
            if (rc != SQLITE_OK) {
                std::cerr << sqlite3_errmsg(db) << std::endl;
                sqlite3_close(db);
                return result;
            }

            sqlite3_bind_text(pstmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);

            while ((rc = sqlite3_step(pstmt)) == SQLITE_ROW) {
                std::map<std::string, std::any> student;
                student["id"] = sqlite3_column_int(pstmt, 0);
                const unsigned char* nameText = sqlite3_column_text(pstmt, 1);
                student["name"] = nameText ? std::string(reinterpret_cast<const char*>(nameText)) : std::string();
                student["age"] = sqlite3_column_int(pstmt, 2);
                const unsigned char* genderText = sqlite3_column_text(pstmt, 3);
                student["gender"] = genderText ? std::string(reinterpret_cast<const char*>(genderText)) : std::string();
                student["grade"] = sqlite3_column_int(pstmt, 4);
                result.push_back(student);
            }

            if (rc != SQLITE_DONE) {
                std::cerr << sqlite3_errmsg(db) << std::endl;
            }

            sqlite3_finalize(pstmt);
            sqlite3_close(db);
        } catch (const std::exception& e) {
            std::cerr << e.what() << std::endl;
            if (pstmt) sqlite3_finalize(pstmt);
            if (db) sqlite3_close(db);
        }

        return result;
    }

    void deleteStudentByName(const std::string& name) {
        const char* deleteQuery = "DELETE FROM students WHERE name = ?";

        sqlite3* db = nullptr;
        sqlite3_stmt* pstmt = nullptr;
        try {
            db = getConnection();
            int rc = sqlite3_prepare_v2(db, deleteQuery, -1, &pstmt, nullptr);
            if (rc != SQLITE_OK) {
                std::cerr << sqlite3_errmsg(db) << std::endl;
                sqlite3_close(db);
                return;
            }

            sqlite3_bind_text(pstmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);

            rc = sqlite3_step(pstmt);
            if (rc != SQLITE_DONE) {
                std::cerr << sqlite3_errmsg(db) << std::endl;
            }

            sqlite3_finalize(pstmt);
            sqlite3_close(db);
        } catch (const std::exception& e) {
            std::cerr << e.what() << std::endl;
            if (pstmt) sqlite3_finalize(pstmt);
            if (db) sqlite3_close(db);
        }
    }
};