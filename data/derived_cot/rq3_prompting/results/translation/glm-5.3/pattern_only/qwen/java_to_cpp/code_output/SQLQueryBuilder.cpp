// SQLQueryBuilder.h — C++ translation of org.example.SQLQueryBuilder
//
// Behavior-preservation notes:
// - java.util.LinkedHashMap keeps insertion order (re-putting an existing key
//   updates the value in place, keeping the original position). std::map would
//   sort keys and silently change output order, so a small insertion-ordered
//   map is used instead.
// - Nullable Java references (`Map where`, `String columns`) map to pointers,
//   so the null checks translate 1:1 (nullptr).
// - columns.split(",\\s*") semantics (Java \\s = [ \t\n\x0B\f\r], trailing
//   empty tokens dropped, no-match returns the whole string, empty string
//   returns {""}) are replicated exactly.

#include <string>
#include <vector>
#include <utility>

namespace org {
namespace example {

// Minimal insertion-ordered map mirroring java.util.LinkedHashMap iteration
// and put semantics for <string, string>.
class LinkedHashMap {
public:
    using Entry = std::pair<std::string, std::string>;

    void put(const std::string& key, const std::string& value) {
        for (Entry& e : entries_) {
            if (e.first == key) {
                e.second = value;  // key keeps its original position
                return;
            }
        }
        entries_.emplace_back(key, value);
    }

    std::string* get(const std::string& key) {
        for (Entry& e : entries_)
            if (e.first == key) return &e.second;
        return nullptr;
    }

    const std::string* get(const std::string& key) const {
        for (const Entry& e : entries_)
            if (e.first == key) return &e.second;
        return nullptr;
    }

    bool isEmpty() const { return entries_.empty(); }

    const std::vector<Entry>& entrySet() const { return entries_; }

private:
    std::vector<Entry> entries_;
};

class SQLQueryBuilder {
private:
    static bool isJavaWhitespace(unsigned char c) {
        // Java regex \s == [ \t\n\x0B\f\r]
        return c == ' ' || c == '\t' || c == '\n' || c == '\x0B' ||
               c == '\f' || c == '\r';
    }

    // Equivalent of Java: s.split(",\\s*") (limit 0).
    static std::vector<std::string> splitColumns(const std::string& s) {
        std::vector<std::string> parts;
        const std::size_t n = s.size();
        std::size_t index = 0;
        std::size_t i = 0;
        bool matched = false;
        while (i < n) {
            if (s[i] == ',') {
                std::size_t j = i + 1;
                while (j < n && isJavaWhitespace(static_cast<unsigned char>(s[j])))
                    ++j;
                parts.push_back(s.substr(index, i - index));
                index = j;
                i = j;
                matched = true;
            } else {
                ++i;
            }
        }
        if (!matched) return {s};          // no separator: whole string, even ""
        parts.push_back(s.substr(index));   // remaining tail (may be empty)
        // Java split (limit 0) discards trailing empty strings.
        while (!parts.empty() && parts.back().empty()) parts.pop_back();
        return parts;
    }

    static void appendWhere(std::string& query, const LinkedHashMap* where) {
        if (where != nullptr && !where->isEmpty()) {
            query += " WHERE ";
            bool first = true;
            for (const LinkedHashMap::Entry& entry : where->entrySet()) {
                if (!first) query += " AND ";
                query += entry.first;
                query += "='";
                query += entry.second;
                query += "'";
                first = false;
            }
        }
    }

public:
    static std::string select(const std::string& table,
                              const std::string* columns,
                              const LinkedHashMap* where) {
        static const std::string star = "*";
        const std::string& cols = (columns != nullptr) ? *columns : star;
        return select(table, splitColumns(cols), where);
    }

    static std::string select(const std::string& table,
                              const std::vector<std::string>& columns,
                              const LinkedHashMap* where) {
        std::string query = "SELECT ";
        if (!columns.empty()) {
            // String.join(", ", columns)
            for (std::size_t i = 0; i < columns.size(); ++i) {
                if (i > 0) query += ", ";
                query += columns[i];
            }
        } else {
            query += "*";
        }
        query += " FROM ";
        query += table;
        appendWhere(query, where);
        return query;
    }

    static std::string insert(const std::string& table, const LinkedHashMap& data) {
        std::string query = "INSERT INTO ";
        query += table;
        query += " (";
        std::string values = " VALUES (";

        bool first = true;
        for (const LinkedHashMap::Entry& entry : data.entrySet()) {
            if (!first) {
                query += ", ";
                values += ", ";
            }
            query += entry.first;
            values += "'";
            values += entry.second;
            values += "'";
            first = false;
        }

        query += ")";
        values += ")";

        return query + values;
    }

    // Java method name `delete` is a C++ keyword; deleteFrom is the mapping.
    static std::string deleteFrom(const std::string& table, const LinkedHashMap* where) {
        std::string query = "DELETE FROM ";
        query += table;
        appendWhere(query, where);
        return query;
    }

    static std::string update(const std::string& table,
                              const LinkedHashMap& data,
                              const LinkedHashMap* where) {
        std::string query = "UPDATE ";
        query += table;
        query += " SET ";

        bool first = true;
        for (const LinkedHashMap::Entry& entry : data.entrySet()) {
            if (!first) query += ", ";
            query += entry.first;
            query += "='";
            query += entry.second;
            query += "'";
            first = false;
        }

        appendWhere(query, where);
        return query;
    }
};

} // namespace example
} // namespace org