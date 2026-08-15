#include <string>
#include <vector>
#include <any>
#include <sstream>
#include <typeinfo>
#include <utility>
#include <initializer_list>
#include <cstddef>

class SqlMap {
public:
    using value_type = std::pair<std::string, std::any>;
    using container_type = std::vector<value_type>;
    using iterator = container_type::iterator;
    using const_iterator = container_type::const_iterator;

    SqlMap() = default;

    SqlMap(std::initializer_list<value_type> init) {
        for (const auto& kv : init) {
            set(kv.first, kv.second);
        }
    }

    void set(const std::string& key, const std::any& value) {
        for (auto& kv : items_) {
            if (kv.first == key) {
                kv.second = value;
                return;
            }
        }
        items_.emplace_back(key, value);
    }

    const_iterator begin() const { return items_.begin(); }
    const_iterator end() const { return items_.end(); }
    iterator begin() { return items_.begin(); }
    iterator end() { return items_.end(); }

    bool empty() const { return items_.empty(); }
    std::size_t size() const { return items_.size(); }

private:
    container_type items_;
};

namespace {

std::string join(const std::vector<std::string>& items, const std::string& delimiter) {
    std::string result;
    for (std::size_t i = 0; i < items.size(); ++i) {
        if (i > 0) result += delimiter;
        result += items[i];
    }
    return result;
}

std::string to_sql_value(const std::any& value) {
    if (value.type() == typeid(std::string)) {
        return std::any_cast<std::string>(value);
    }
    if (value.type() == typeid(const char*)) {
        return std::any_cast<const char*>(value);
    }
    if (value.type() == typeid(char*)) {
        return std::any_cast<char*>(value);
    }
    if (value.type() == typeid(bool)) {
        return std::any_cast<bool>(value) ? "True" : "False";
    }
    if (value.type() == typeid(int)) {
        return std::to_string(std::any_cast<int>(value));
    }
    if (value.type() == typeid(long)) {
        return std::to_string(std::any_cast<long>(value));
    }
    if (value.type() == typeid(long long)) {
        return std::to_string(std::any_cast<long long>(value));
    }
    if (value.type() == typeid(unsigned int)) {
        return std::to_string(std::any_cast<unsigned int>(value));
    }
    if (value.type() == typeid(unsigned long)) {
        return std::to_string(std::any_cast<unsigned long>(value));
    }
    if (value.type() == typeid(unsigned long long)) {
        return std::to_string(std::any_cast<unsigned long long>(value));
    }
    if (value.type() == typeid(float)) {
        std::ostringstream oss;
        oss << std::any_cast<float>(value);
        std::string s = oss.str();
        if (s.find('.') == std::string::npos && s.find('e') == std::string::npos && s.find('E') == std::string::npos) {
            s += ".0";
        }
        return s;
    }
    if (value.type() == typeid(double)) {
        std::ostringstream oss;
        oss << std::any_cast<double>(value);
        std::string s = oss.str();
        if (s.find('.') == std::string::npos && s.find('e') == std::string::npos && s.find('E') == std::string::npos) {
            s += ".0";
        }
        return s;
    }
    return "";
}

std::string format_conditions(const SqlMap& where) {
    std::vector<std::string> conditions;
    for (const auto& kv : where) {
        conditions.push_back(kv.first + "='" + to_sql_value(kv.second) + "'");
    }
    return join(conditions, " AND ");
}

std::string format_set(const SqlMap& data) {
    std::vector<std::string> sets;
    for (const auto& kv : data) {
        sets.push_back(kv.first + "='" + to_sql_value(kv.second) + "'");
    }
    return join(sets, ", ");
}

} // namespace

class SQLQueryBuilder {
public:
    static std::string select(const std::string& table, const std::string& columns = "*", const SqlMap& where = {}) {
        std::string query = "SELECT " + columns + " FROM " + table;
        if (!where.empty()) {
            query += " WHERE " + format_conditions(where);
        }
        return query;
    }

    static std::string select(const std::string& table, const std::vector<std::string>& columns, const SqlMap& where = {}) {
        std::string cols = join(columns, ", ");
        std::string query = "SELECT " + cols + " FROM " + table;
        if (!where.empty()) {
            query += " WHERE " + format_conditions(where);
        }
        return query;
    }

    static std::string insert(const std::string& table, const SqlMap& data) {
        std::vector<std::string> keys;
        std::vector<std::string> values;
        for (const auto& kv : data) {
            keys.push_back(kv.first);
            values.push_back("'" + to_sql_value(kv.second) + "'");
        }
        return "INSERT INTO " + table + " (" + join(keys, ", ") + ") VALUES (" + join(values, ", ") + ")";
    }

    static std::string delete_(const std::string& table, const SqlMap& where = {}) {
        std::string query = "DELETE FROM " + table;
        if (!where.empty()) {
            query += " WHERE " + format_conditions(where);
        }
        return query;
    }

    static std::string update(const std::string& table, const SqlMap& data, const SqlMap& where = {}) {
        std::string query = "UPDATE " + table + " SET " + format_set(data);
        if (!where.empty()) {
            query += " WHERE " + format_conditions(where);
        }
        return query;
    }
};