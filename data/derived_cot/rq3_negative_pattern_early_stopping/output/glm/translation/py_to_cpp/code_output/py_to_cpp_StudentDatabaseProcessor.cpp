#include <string>
#include <vector>
#include <tuple>
#include <map>
#include <variant>
#include <sqlite3.h>

class StudentDatabaseProcessor {
public:
    StudentDatabaseProcessor(const std::string& database_name)
        : database_name(database_name) {}

    void create_student_table() {
        sqlite3* db;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            sqlite3_close(db);
            return;
        }

        const char* create_table_query =
            "CREATE TABLE IF NOT EXISTS students ("
            "id INTEGER PRIMARY KEY,"
            "name TEXT,"
            "age INTEGER,"
            "gender TEXT,"
            "grade INTEGER"
            ")";

        char* errmsg = nullptr;
        sqlite3_exec(db, create_table_query, nullptr, nullptr, &errmsg);
        if (errmsg) {
            sqlite3_free(errmsg);
        }
        sqlite3_close(db);
    }

    void insert_student(const std::map<std::string, std::variant<int, std::string>>& student_data) {
        sqlite3* db;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            sqlite3_close(db);
            return;
        }

        const char* insert_query =
            "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)";

        sqlite3_stmt* stmt;
        rc = sqlite3_prepare_v2(db, insert_query, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            sqlite3_close(db);
            return;
        }

        const std::string& name = std::get<std::string>(student_data.at("name"));
        int age = std::get<int>(student_data.at("age"));
        const std::string& gender = std::get<std::string>(student_data.at("gender"));
        int grade = std::get<int>(student_data.at("grade"));

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_int(stmt, 2, age);
        sqlite3_bind_text(stmt, 3, gender.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_int(stmt, 4, grade);

        sqlite3_step(stmt);
        sqlite3_finalize(stmt);
        sqlite3_close(db);
    }

    std::vector<std::tuple<int, std::string, int, std::string, int>> search_student_by_name(const std::string& name) {
        std::vector<std::tuple<int, std::string, int, std::string, int>> result;

        sqlite3* db;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            sqlite3_close(db);
            return result;
        }

        const char* select_query = "SELECT * FROM students WHERE name = ?";

        sqlite3_stmt* stmt;
        rc = sqlite3_prepare_v2(db, select_query, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            sqlite3_close(db);
            return result;
        }

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);

        while (sqlite3_step(stmt) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);

            std::string name_val;
            const unsigned char* name_ptr = sqlite3_column_text(stmt, 1);
            if (name_ptr) {
                name_val = reinterpret_cast<const char*>(name_ptr);
            }

            int age = sqlite3_column_int(stmt, 2);

            std::string gender;
            const unsigned char* gender_ptr = sqlite3_column_text(stmt, 3);
            if (gender_ptr) {
                gender = reinterpret_cast<const char*>(gender_ptr);
            }

            int grade = sqlite3_column_int(stmt, 4);

            result.emplace_back(id, name_val, age, gender, grade);
        }

        sqlite3_finalize(stmt);
        sqlite3_close(db);

        return result;
    }

    void delete_student_by_name(const std::string& name) {
        sqlite3* db;
        int rc = sqlite3_open(database_name.c_str(), &db);
        if (rc != SQLITE_OK) {
            sqlite3_close(db);
            return;
        }

        const char* delete_query = "DELETE FROM students WHERE name = ?";

        sqlite3_stmt* stmt;
        rc = sqlite3_prepare_v2(db, delete_query, -1, &stmt, nullptr);
        if (rc != SQLITE_OK) {
            sqlite3_close(db);
            return;
        }

        sqlite3_bind_text(stmt, 1, name.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_step(stmt);
        sqlite3_finalize(stmt);
        sqlite3_close(db);
    }

private:
    std::string database_name;
};