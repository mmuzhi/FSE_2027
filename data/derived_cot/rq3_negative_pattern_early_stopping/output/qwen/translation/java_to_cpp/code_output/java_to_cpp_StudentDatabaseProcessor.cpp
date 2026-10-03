#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <any>
#include <stdexcept>
#include <sqlite3.h>

class StudentDatabaseProcessor {
private:
    std::string databaseName;

    struct DatabaseConnection {
        sqlite3* db;
        DatabaseConnection(const std::string& dbName) {
            int rc = sqlite3_open(dbName.c_str(), &db);
            if (rc != SQLITE_OK) {
                throw std::runtime_error(sqlite3_errmsg(db));
            }
        }
        ~DatabaseConnection() {
            if (db) {
                sqlite3_close(db);
            }
        }
        sqlite3* get() const { return db; }
    };

    struct PreparedStatement {
        DatabaseConnection& conn;
        sqlite3_stmt* stmt;
        PreparedStatement(DatabaseConnection& conn, const std::string& query) : conn(conn), stmt(nullptr) {
            int rc = sqlite3_prepare_v2(conn.get(), query.c_str(), -1, &stmt, nullptr);
            if (rc != SQLITE_OK) {
                throw std::runtime_error(sqlite3_errmsg(conn.get()));
            }
        }
        ~PreparedStatement() {
            if (stmt) {
                sqlite3_finalize(stmt);
            }
        }
        bool execute() const {
            int rc = sqlite3_step(stmt);
            if (rc == SQLITE_DONE || rc == SQLITE_ROW) {
                return true;
            }
            throw std::runtime_error(sqlite3_errmsg(conn.get()));
        }
        int executeUpdate() const {
            int rc = sqlite3_step(stmt);
            if (rc == SQLITE_DONE) {
                return sqlite3_changes(conn.get());
            }
            throw std::runtime_error(sqlite3_errmsg(conn.get()));
        }
        operator bool() const {
            return sqlite3_step(stmt) == SQLITE_ROW;
        }
    };

    struct ResultSet {
        PreparedStatement& pstmt;
        ResultSet(PreparedStatement& pstmt) : pstmt(pstmt) {}
        ~ResultSet() {
            if (sqlite3_step(pstmt.stmt) != SQLITE_DONE) {
                // Final step to clear remaining rows
            }
        }
        int getInt(const std::string& columnName) const {
            int value = sqlite3_column_int(pstmt.stmt, sqlite3_column_index(pstmt.stmt, columnName.c_str()));
            return value;
        }
        const char* getString(const std::string& columnName) const {
            return reinterpret_cast<const char*>(sqlite3_column_text(pstmt.stmt, sqlite3_column_index(pstmt.stmt, columnName.c_str())));
        }
    };

public:
    explicit StudentDatabaseProcessor(const std::string& databaseName) : databaseName(databaseName) {}

    void createStudentTable() {
        std::string createTableQuery = "CREATE TABLE IF NOT EXISTS students ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT, "
                "age INTEGER, "
                "gender TEXT, "
                "grade INTEGER"
                ")";
        try (DatabaseConnection conn(databaseName);
             PreparedStatement pstmt(conn, createTableQuery)) {
            pstmt.execute();
        } catch (const std::exception& e) {
            std::cerr << e.what() << std::endl;
        }
    }

    void insertStudent(const StudentData& studentData) {
        std::string insertQuery = "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)";
        try (DatabaseConnection conn(databaseName);
             PreparedStatement pstmt(conn, insertQuery)) {
            pstmt.setString(1, studentData.name);
            pstmt.setInt(2, studentData.age);
            pstmt.setString(3, studentData.gender);
            pstmt.setInt(4, studentData.grade);
            pstmt.executeUpdate();
        } catch (const std::exception& e) {
            std::cerr << e.what() << std::endl;
        }
    }

    std::vector<std::map<std::string, std::any>> searchStudentByName(const std::string& name) {
        std::string selectQuery = "SELECT * FROM students WHERE name = ?";
        std::vector<std::map<std::string, std::any>> result;
        try (DatabaseConnection conn(databaseName);
             PreparedStatement pstmt(conn, selectQuery)) {
            pstmt.setString(1, name);
            while (PreparedStatement pstmt(conn, selectQuery)) {
                std::map<std::string, std::any> student;
                student["id"] = pstmt.getInt("id");
                student["name"] = pstmt.getString("name");
                student["age"] = pstmt.getInt("age");
                student["gender"] = pstmt.getString("gender");
                student["grade"] = pstmt.getInt("grade");
                result.push_back(student);
            }
        } catch (const std::exception& e) {
            std::cerr << e.what() << std::endl;
        }
        return result;
    }

    void deleteStudentByName(const std::string& name) {
        std::string deleteQuery = "DELETE FROM students WHERE name = ?";
        try (DatabaseConnection conn(databaseName);
             PreparedStatement pstmt(conn, deleteQuery)) {
            pstmt.setString(1, name);
            pstmt.executeUpdate();
        } catch (const std::exception& e) {
            std::cerr << e.what() << std::endl;
        }
    }

    struct StudentData {
        std::string name;
        int age;
        std::string gender;
        int grade;

        StudentData(const std::string& name, int age, const std::string& gender, int grade)
            : name(name), age(age), gender(gender), grade(grade) {}

        const std::string& getName() const { return name; }
        int getAge() const { return age; }
        const std::string& getGender() const { return gender; }
        int getGrade() const { return grade; }
    };
};

int main() {
    StudentDatabaseProcessor processor("students.db");
    processor.createStudentTable();
    processor.insertStudent(StudentData("Alice", 20, "F", 90));
    auto students = processor.searchStudentByName("Alice");
    for (const auto& student : students) {
        std::cout << "ID: " << std::any_cast<int>(student["id"]) << std::endl;
    }
    processor.deleteStudentByName("Alice");
    return 0;
}