#include <sqlite3.h>

#include <any>
#include <iostream>
#include <map>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

class StudentDatabaseProcessor {
public:
    explicit StudentDatabaseProcessor(std::string databaseName)
        : databaseName_(std::move(databaseName)) {}

    void createStudentTable() {
        const char* createTableQuery =
            "CREATE TABLE IF NOT EXISTS students ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT, "
            "age INTEGER, "
            "gender TEXT, "
            "grade INTEGER"
            ")";
        try {
            sqlite3* conn = getConnection();
            char* errMsg = nullptr;
            if (sqlite3_exec(conn, createTableQuery, nullptr, nullptr, &errMsg) != SQLITE_OK) {
                std::string msg = errMsg ? errMsg : sqlite3_errmsg(conn);
                sqlite3_free(errMsg);
                sqlite3_close(conn);
                throw std::runtime_error(msg);
            }
            sqlite3_close(conn);
        } catch (const std::exception& e) {
            std::cerr << e.what() << std::endl;
        }
    }

    void insertStudent(const StudentData& studentData) {
        const char* insertQuery =
            "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)";
        sqlite3* conn = nullptr;
        sqlite3_stmt* pstmt = nullptr;
        try {
            conn = getConnection();
            if (sqlite3_prepare_v2(conn, insertQuery, -1, &pstmt, nullptr) != SQLITE_OK) {
                throw std::runtime_error(sqlite3_errmsg(conn));
            }
            sqlite3_bind_text(pstmt, 1, studentData.getName().c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_bind_int(pstmt, 2, studentData.getAge());
            sqlite3_bind_text(pstmt, 3, studentData.getGender().c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_bind_int(pstmt, 4, studentData.getGrade());
            if (sqlite3_step(pstmt) != SQLITE_DONE) {
                throw std::runtime_error(sqlite3_errmsg(conn));
            }
            sqlite3_finalize(pstmt);
            sqlite3_close(conn);
        } catch (const std::exception& e) {
            if (pstmt) sqlite3_finalize(pstmt);
            if (conn) sqlite3_close(conn);
            std::cerr << e.what() << std::endl;
        }
    }

    std::vector<std::map<std::string, std::any>> searchStudentByName(const std::string& name) {
        const char* selectQuery = "SELECT * FROM students WHERE name = ?";
        std::vector<std::map<std::string, std::any>> result;
        sqlite3* conn = nullptr;
        sqlite3_stmt* pstmt = nullptr;
        try {
            conn = getConnection();
            if (sqlite3_prepare_v2(conn, selectQuery, -1, &pstmt, nullptr) != SQLITE_OK) {
                throw std::runtime_error(sqlite3_errmsg(conn));
            }
            sqlite3_bind_text(pstmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);
            while (sqlite3_step(pstmt) == SQLITE_ROW) {
                std::map<std::string, std::any> student;
                student.emplace("id", sqlite3_column_int(pstmt, 0));
                student.emplace("name", textColumn(pstmt, 1));
                student.emplace("age", sqlite3_column_int(pstmt, 2));
                student.emplace("gender", textColumn(pstmt, 3));
                student.emplace("grade", sqlite3_column_int(pstmt, 4));
                result.push_back(std::move(student));
            }
            sqlite3_finalize(pstmt);
            sqlite3_close(conn);
        } catch (const std::exception& e) {
            if (pstmt) sqlite3_finalize(pstmt);
            if (conn) sqlite3_close(conn);
            std::cerr << e.what() << std::endl;
        }
        return result;
    }

    void deleteStudentByName(const std::string& name) {
        const char* deleteQuery = "DELETE FROM students WHERE name = ?";
        sqlite3* conn = nullptr;
        sqlite3_stmt* pstmt = nullptr;
        try {
            conn = getConnection();
            if (sqlite3_prepare_v2(conn, deleteQuery, -1, &pstmt, nullptr) != SQLITE_OK) {
                throw std::runtime_error(sqlite3_errmsg(conn));
            }
            sqlite3_bind_text(pstmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);
            if (sqlite3_step(pstmt) != SQLITE_DONE) {
                throw std::runtime_error(sqlite3_errmsg(conn));
            }
            sqlite3_finalize(pstmt);
            sqlite3_close(conn);
        } catch (const std::exception& e) {
            if (pstmt) sqlite3_finalize(pstmt);
            if (conn) sqlite3_close(conn);
            std::cerr << e.what() << std::endl;
        }
    }

    class StudentData {
    public:
        StudentData(std::string name, int age, std::string gender, int grade)
            : name_(std::move(name)), age_(age), gender_(std::move(gender)), grade_(grade) {}

        const std::string& getName() const { return name_; }
        int getAge() const { return age_; }
        const std::string& getGender() const { return gender_; }
        int getGrade() const { return grade_; }

    private:
        std::string name_;
        int age_;
        std::string gender_;
        int grade_;
    };

private:
    std::string databaseName_;

    sqlite3* getConnection() {
        sqlite3* conn = nullptr;
        if (sqlite3_open(("file:" + databaseName_ + "?nolocale=1").c_str(), &conn) != SQLITE_OK) {
            std::string msg = conn ? sqlite3_errmsg(conn) : "unable to open database";
            if (conn) sqlite3_close(conn);
            throw std::runtime_error(msg);
        }
        return conn;
    }

    static std::string textColumn(sqlite3_stmt* stmt, int col) {
        const unsigned char* text = sqlite3_column_text(stmt, col);
        return text ? std::string(reinterpret_cast<const char*>(text)) : std::string();
    }
};