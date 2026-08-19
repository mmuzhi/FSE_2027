#include <sqlite3.h>

#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <variant>
#include <vector>

namespace org {
namespace example {

class StudentDatabaseProcessor {
public:
    static class StudentData {
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

private:
    std::string databaseName;

    // Equivalent of DriverManager.getConnection("jdbc:sqlite:" + databaseName).
    // Throws std::runtime_error in place of SQLException on failure.
    sqlite3* getConnection() {
        sqlite3* conn = nullptr;
        int rc = sqlite3_open(databaseName.c_str(), &conn);
        if (rc != SQLITE_OK) {
            if (conn != nullptr) sqlite3_close(conn);
            throw std::runtime_error(
                std::string("[SQLITE] ") + sqlite3_errstr(rc) +
                ", error code: " + std::to_string(rc));
        }
        return conn;
    }

    static std::string columnText(sqlite3_stmt* stmt, int col) {
        const unsigned char* text = sqlite3_column_text(stmt, col);
        return text != nullptr ? std::string(reinterpret_cast<const char*>(text)) : std::string();
    }

public:
    explicit StudentDatabaseProcessor(const std::string& databaseName)
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
        sqlite3* conn = nullptr;
        sqlite3_stmt* stmt = nullptr;
        char* errMsg = nullptr;
        try {
            conn = getConnection();
            int rc = sqlite3_exec(conn, createTableQuery, nullptr, nullptr, &errMsg);
            if (rc != SQLITE_OK) {
                // Equivalent of e.printStackTrace(): report error to stderr and continue.
                std::cerr << "[SQLITE] "
                          << (errMsg != nullptr ? errMsg : sqlite3_errmsg(conn))
                          << std::endl;
            }
        } catch (const std::exception& e) {
            std::cerr << e.what() << std::endl;
        }
        if (errMsg != nullptr) sqlite3_free(errMsg);
        if (stmt != nullptr) sqlite3_finalize(stmt);
        if (conn != nullptr) sqlite3_close(conn);
    }

    void insertStudent(const StudentData& studentData) {
        const char* insertQuery =
            "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)";
        sqlite3* conn = nullptr;
        sqlite3_stmt* pstmt = nullptr;
        try {
            conn = getConnection();
            int rc = sqlite3_prepare_v2(conn, insertQuery, -1, &pstmt, nullptr);
            if (rc == SQLITE_OK) {
                sqlite3_bind_text(pstmt, 1, studentData.getName().c_str(), -1, SQLITE_TRANSIENT);
                sqlite3_bind_int(pstmt, 2, studentData.getAge());
                sqlite3_bind_text(pstmt, 3, studentData.getGender().c_str(), -1, SQLITE_TRANSIENT);
                sqlite3_bind_int(pstmt, 4, studentData.getGrade());
                rc = sqlite3_step(pstmt);
                if (rc != SQLITE_DONE) {
                    std::cerr << "[SQLITE] " << sqlite3_errmsg(conn) << std::endl;
                }
            } else {
                std::cerr << "[SQLITE] " << sqlite3_errmsg(conn) << std::endl;
            }
        } catch (const std::exception& e) {
            std::cerr << e.what() << std::endl;
        }
        if (pstmt != nullptr) sqlite3_finalize(pstmt);
        if (conn != nullptr) sqlite3_close(conn);
    }

    // std::variant<int, std::string> models Java's Map<String, Object>
    // (values are either Integer or String, never null via this API).
    std::vector<std::map<std::string, std::variant<int, std::string>>> searchStudentByName(
        const std::string& name) {
        const char* selectQuery = "SELECT * FROM students WHERE name = ?";
        std::vector<std::map<std::string, std::variant<int, std::string>>> result;
        sqlite3* conn = nullptr;
        sqlite3_stmt* pstmt = nullptr;
        try {
            conn = getConnection();
            int rc = sqlite3_prepare_v2(conn, selectQuery, -1, &pstmt, nullptr);
            if (rc == SQLITE_OK) {
                sqlite3_bind_text(pstmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);
                while ((rc = sqlite3_step(pstmt)) == SQLITE_ROW) {
                    std::map<std::string, std::variant<int, std::string>> student;
                    student["id"] = static_cast<int>(sqlite3_column_int64(pstmt, 0));
                    student["name"] = columnText(pstmt, 1);
                    student["age"] = sqlite3_column_int(pstmt, 2);
                    student["gender"] = columnText(pstmt, 3);
                    student["grade"] = sqlite3_column_int(pstmt, 4);
                    result.push_back(std::move(student));
                }
                if (rc != SQLITE_DONE) {
                    std::cerr << "[SQLITE] " << sqlite3_errmsg(conn) << std::endl;
                }
            } else {
                std::cerr << "[SQLITE] " << sqlite3_errmsg(conn) << std::endl;
            }
        } catch (const std::exception& e) {
            std::cerr << e.what() << std::endl;
        }
        if (pstmt != nullptr) sqlite3_finalize(pstmt);
        if (conn != nullptr) sqlite3_close(conn);
        return result;
    }

    void deleteStudentByName(const std::string& name) {
        const char* deleteQuery = "DELETE FROM students WHERE name = ?";
        sqlite3* conn = nullptr;
        sqlite3_stmt* pstmt = nullptr;
        try {
            conn = getConnection();
            int rc = sqlite3_prepare_v2(conn, deleteQuery, -1, &pstmt, nullptr);
            if (rc == SQLITE_OK) {
                sqlite3_bind_text(pstmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);
                rc = sqlite3_step(pstmt);
                if (rc != SQLITE_DONE) {
                    std::cerr << "[SQLITE] " << sqlite3_errmsg(conn) << std::endl;
                }
            } else {
                std::cerr << "[SQLITE] " << sqlite3_errmsg(conn) << std::endl;
            }
        } catch (const std::exception& e) {
            std::cerr << e.what() << std::endl;
        }
        if (pstmt != nullptr) sqlite3_finalize(pstmt);
        if (conn != nullptr) sqlite3_close(conn);
    }
};

}  // namespace example
}  // namespace org