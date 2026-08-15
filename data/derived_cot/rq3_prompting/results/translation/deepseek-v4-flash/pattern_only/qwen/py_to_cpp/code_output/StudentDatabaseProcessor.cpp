#include <sqlite3.h>
#include <cstdint>
#include <map>
#include <memory>
#include <optional>
#include <stdexcept>
#include <string>
#include <tuple>
#include <variant>
#include <vector>

class StudentDatabaseProcessor {
public:
    using StudentData = std::map<std::string, std::variant<int64_t, std::string>>;
    using StudentRow = std::tuple<
        std::optional<int64_t>,
        std::optional<std::string>,
        std::optional<int64_t>,
        std::optional<std::string>,
        std::optional<int64_t>>;

    explicit StudentDatabaseProcessor(const std::string& database_name)
        : database_name_(database_name) {}

    void create_student_table() {
        auto db = open_database();
        char* errMsg = nullptr;
        int rc = sqlite3_exec(
            db.get(),
            "CREATE TABLE IF NOT EXISTS students ("
            "id INTEGER PRIMARY KEY, "
            "name TEXT, "
            "age INTEGER, "
            "gender TEXT, "
            "grade INTEGER)",
            nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            std::string msg = errMsg ? errMsg : "SQL error";
            sqlite3_free(errMsg);
            throw std::runtime_error(msg);
        }
    }

    void insert_student(const StudentData& student_data) {
        auto db = open_database();
        const char* sql = "INSERT INTO students (name, age, gender, grade) VALUES (?, ?, ?, ?)";
        sqlite3_stmt* raw_stmt = nullptr;
        int rc = sqlite3_prepare_v2(db.get(), sql, -1, &raw_stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db.get()));
        }
        std::unique_ptr<sqlite3_stmt, decltype(&sqlite3_finalize)> stmt(raw_stmt, &sqlite3_finalize);

        std::string name = get_string(student_data, "name");
        int64_t age = get_int(student_data, "age");
        std::string gender = get_string(student_data, "gender");
        int64_t grade = get_int(student_data, "grade");

        rc = sqlite3_bind_text(stmt.get(), 1, name.c_str(), -1, SQLITE_TRANSIENT);
        if (rc != SQLITE_OK) throw std::runtime_error(sqlite3_errmsg(db.get()));
        rc = sqlite3_bind_int64(stmt.get(), 2, age);
        if (rc != SQLITE_OK) throw std::runtime_error(sqlite3_errmsg(db.get()));
        rc = sqlite3_bind_text(stmt.get(), 3, gender.c_str(), -1, SQLITE_TRANSIENT);
        if (rc != SQLITE_OK) throw std::runtime_error(sqlite3_errmsg(db.get()));
        rc = sqlite3_bind_int64(stmt.get(), 4, grade);
        if (rc != SQLITE_OK) throw std::runtime_error(sqlite3_errmsg(db.get()));

        rc = sqlite3_step(stmt.get());
        if (rc != SQLITE_DONE) {
            throw std::runtime_error(sqlite3_errmsg(db.get()));
        }
    }

    std::vector<StudentRow> search_student_by_name(const std::string& name) {
        auto db = open_database();
        const char* sql = "SELECT * FROM students WHERE name = ?";
        sqlite3_stmt* raw_stmt = nullptr;
        int rc = sqlite3_prepare_v2(db.get(), sql, -1, &raw_stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db.get()));
        }
        std::unique_ptr<sqlite3_stmt, decltype(&sqlite3_finalize)> stmt(raw_stmt, &sqlite3_finalize);

        rc = sqlite3_bind_text(stmt.get(), 1, name.c_str(), -1, SQLITE_TRANSIENT);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db.get()));
        }

        std::vector<StudentRow> result;
        while ((rc = sqlite3_step(stmt.get())) == SQLITE_ROW) {
            std::optional<int64_t> id = get_optional_int(stmt.get(), 0);
            std::optional<std::string> name_opt = get_optional_text(stmt.get(), 1);
            std::optional<int64_t> age = get_optional_int(stmt.get(), 2);
            std::optional<std::string> gender = get_optional_text(stmt.get(), 3);
            std::optional<int64_t> grade = get_optional_int(stmt.get(), 4);
            result.emplace_back(id, name_opt, age, gender, grade);
        }
        if (rc != SQLITE_DONE) {
            throw std::runtime_error(sqlite3_errmsg(db.get()));
        }
        return result;
    }

    void delete_student_by_name(const std::string& name) {
        auto db = open_database();
        const char* sql = "DELETE FROM students WHERE name = ?";
        sqlite3_stmt* raw_stmt = nullptr;
        int rc = sqlite3_prepare_v2(db.get(), sql, -1, &raw_stmt, nullptr);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db.get()));
        }
        std::unique_ptr<sqlite3_stmt, decltype(&sqlite3_finalize)> stmt(raw_stmt, &sqlite3_finalize);

        rc = sqlite3_bind_text(stmt.get(), 1, name.c_str(), -1, SQLITE_TRANSIENT);
        if (rc != SQLITE_OK) {
            throw std::runtime_error(sqlite3_errmsg(db.get()));
        }

        rc = sqlite3_step(stmt.get());
        if (rc != SQLITE_DONE) {
            throw std::runtime_error(sqlite3_errmsg(db.get()));
        }
    }

private:
    std::string database_name_;

    std::unique_ptr<sqlite3, decltype(&sqlite3_close)> open_database() {
        sqlite3* raw_db = nullptr;
        int rc = sqlite3_open(database_name_.c_str(), &raw_db);
        if (rc != SQLITE_OK) {
            std::string msg = raw_db ? sqlite3_errmsg(raw_db) : "Failed to open database";
            if (raw_db) sqlite3_close(raw_db);
            throw std::runtime_error(msg);
        }
        return std::unique_ptr<sqlite3, decltype(&sqlite3_close)>(raw_db, &sqlite3_close);
    }

    static std::string get_string(const StudentData& data, const std::string& key) {
        auto it = data.find(key);
        if (it == data.end()) {
            throw std::out_of_range("Key not found: " + key);
        }
        if (!std::holds_alternative<std::string>(it->second)) {
            throw std::runtime_error("Key " + key + " is not a string");
        }
        return std::get<std::string>(it->second);
    }

    static int64_t get_int(const StudentData& data, const std::string& key) {
        auto it = data.find(key);
        if (it == data.end()) {
            throw std::out_of_range("Key not found: " + key);
        }
        if (!std::holds_alternative<int64_t>(it->second)) {
            throw std::runtime_error("Key " + key + " is not an int");
        }
        return std::get<int64_t>(it->second);
    }

    static std::optional<int64_t> get_optional_int(sqlite3_stmt* stmt, int col) {
        if (sqlite3_column_type(stmt, col) == SQLITE_NULL) {
            return std::nullopt;
        }
        return sqlite3_column_int64(stmt, col);
    }

    static std::optional<std::string> get_optional_text(sqlite3_stmt* stmt, int col) {
        if (sqlite3_column_type(stmt, col) == SQLITE_NULL) {
            return std::nullopt;
        }
        const unsigned char* text = sqlite3_column_text(stmt, col);
        return std::string(reinterpret_cast<const char*>(text));
    }
};