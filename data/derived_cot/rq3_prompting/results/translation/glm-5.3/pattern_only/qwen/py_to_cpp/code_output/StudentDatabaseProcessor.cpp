#include <sqlite3.h>

#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

class StudentDatabaseProcessor {
public:
    // Mirrors the Python dict {'name': str, 'age': int, 'gender': str, 'grade': int}
    struct StudentData {
        std::string name;
        int age;
        std::string gender;
        int grade;
    };

    // Row shape of the "students" table: (id, name, age, gender, grade)
    using StudentRow = std::tuple<int, std::string, int, std::string, int>;

    explicit StudentDatabaseProcessor(std::string database_name)
        : database_name(std::move(database_name)) {}

    void create_student_table() {
        sqlite3* conn = open_connection();

        const char* create_table_query =
            "CREATE TABLE IF NOT EXISTS students ("
            "id INTEGER PRIMARY KEY,"
            "name TEXT,"
            "age INTEGER,"
            "gender TEXT,"
            "grade INTEGER"
            ")";

        char* err_msg = nullptr;
        if (sqlite3_exec(conn, create_table_query, nullptr, nullptr, &err_msg) != SQLITE_OK) {
            std::string msg = err_msg ? err_msg : sqlite3_errmsg(conn);
            sqlite3_free(err_msg);
            sqlite3_close(conn);
            throw std::runtime_error(msg);  // corresponds to sqlite3 raising an exception
        }
        sqlite3_free(err_msg);
        sqlite3_close(conn);  // autocommit mode: statement already committed
    }

    void insert_student(const StudentData& student_data) {
        sqlite3* conn = open_connection();

        const char* insert_query =
            "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(conn, insert_query, -1, &stmt, nullptr) != SQLITE_OK) {
            std::string msg = sqlite3_errmsg(conn);
            sqlite3_close(conn);
            throw std::runtime_error(msg);
        }

        sqlite3_bind_text(stmt, 1, student_data.name.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_int(stmt, 2, student_data.age);
        sqlite3_bind_text(stmt, 3, student_data.gender.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_int(stmt, 4, student_data.grade);

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(conn);
            sqlite3_finalize(stmt);
            sqlite3_close(conn);
            throw std::runtime_error(msg);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(conn);  // closing commits (autocommit), like conn.commit(); conn.close()
    }

    std::vector<StudentRow> search_student_by_name(const std::string& name) {
        sqlite3* conn = open_connection();

        const char* select_query = "SELECT * FROM students WHERE name = ?";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(conn, select_query, -1, &stmt, nullptr) != SQLITE_OK) {
            std::string msg = sqlite3_errmsg(conn);
            sqlite3_close(conn);
            throw std::runtime_error(msg);
        }

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);

        std::vector<StudentRow> result;
        int rc;
        while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
            // Column order matches table definition: id, name, age, gender, grade
            result.emplace_back(
                sqlite3_column_int(stmt, 0),
                column_text(stmt, 1),
                sqlite3_column_int(stmt, 2),
                column_text(stmt, 3),
                sqlite3_column_int(stmt, 4));
        }
        if (rc != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(conn);
            sqlite3_finalize(stmt);
            sqlite3_close(conn);
            throw std::runtime_error(msg);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(conn);  // no commit in the Python version either

        return result;
    }

    void delete_student_by_name(const std::string& name) {
        sqlite3* conn = open_connection();

        const char* delete_query = "DELETE FROM students WHERE name = ?";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(conn, delete_query, -1, &stmt, nullptr) != SQLITE_OK) {
            std::string msg = sqlite3_errmsg(conn);
            sqlite3_close(conn);
            throw std::runtime_error(msg);
        }

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);

        if (sqlite3_step(stmt) != SQLITE_DONE) {
            std::string msg = sqlite3_errmsg(conn);
            sqlite3_finalize(stmt);
            sqlite3_close(conn);
            throw std::runtime_error(msg);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(conn);  // closing commits (autocommit), like conn.commit(); conn.close()
    }

private:
    std::string database_name;

    sqlite3* open_connection() const {
        sqlite3* conn = nullptr;
        if (sqlite3_open(database_name.c_str(), &conn) != SQLITE_OK) {
            std::string msg = conn ? sqlite3_errmsg(conn) : "unable to open database";
            if (conn) sqlite3_close(conn);
            throw std::runtime_error(msg);  // corresponds to sqlite3.connect raising
        }
        return conn;
    }

    static std::string column_text(sqlite3_stmt* stmt, int col) {
        const unsigned char* text = sqlite3_column_text(stmt, col);
        return text ? reinterpret_cast<const char*>(text) : std::string();  // NULL -> empty
    }
};