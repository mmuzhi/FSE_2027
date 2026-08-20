#include <map>
#include <memory>
#include <set>
#include <string>
#include <utility>
#include <variant>

namespace org::example {

// C++ analogue of Java's `Object` used as the map value type.
// It can hold null, a Boolean, an Integer, a Double, a String, or a shared
// reference to a Map<String, Object>. The shared_ptr mirrors Java reference
// semantics (maps are aliased, not copied; lifetime is GC-like).
struct Object;
using EmployeeInfo = std::map<std::string, Object>;

struct Object {
    std::variant<std::monostate, bool, int, double, std::string,
                 std::shared_ptr<EmployeeInfo>>
        value;

    Object() = default;                                        // null
    Object(bool v) : value(v) {}                               // Boolean
    Object(int v) : value(v) {}                                // Integer
    Object(double v) : value(v) {}                             // Double
    Object(const std::string& v) : value(v) {}                 // String
    Object(std::string&& v) : value(std::move(v)) {}           // String
    Object(const char* v) : value(std::string(v)) {}           // String literal
    Object(const std::shared_ptr<EmployeeInfo>& v) : value(v) {}
    Object(std::shared_ptr<EmployeeInfo>&& v) : value(std::move(v)) {}
};

class HRManagementSystem {
public:
    std::map<int, std::shared_ptr<EmployeeInfo>> employees;

    HRManagementSystem() = default;

    bool addEmployee(int employeeId, const std::string& name,
                     const std::string& position,
                     const std::string& department, double salary) {
        if (employees.find(employeeId) != employees.end()) {
            return false;
        }
        auto employeeInfo = std::make_shared<EmployeeInfo>();
        (*employeeInfo)["name"] = name;
        (*employeeInfo)["position"] = position;
        (*employeeInfo)["department"] = department;
        (*employeeInfo)["salary"] = salary;
        employees.emplace(employeeId, std::move(employeeInfo));
        return true;
    }

    bool removeEmployee(int employeeId) {
        auto it = employees.find(employeeId);
        if (it != employees.end()) {
            employees.erase(it);
            return true;
        } else {
            return false;
        }
    }

    bool updateEmployee(int employeeId,
                        const EmployeeInfo& updatedEmployeeInfo) {
        auto it = employees.find(employeeId);
        if (it == employees.end()) {
            return false;
        } else {
            static const std::set<std::string> validKeys = {
                "name", "position", "department", "salary"};
            // Validate every key first; reject without modifying anything
            // if any key is invalid (same as the Java version).
            for (const auto& entry : updatedEmployeeInfo) {
                if (validKeys.find(entry.first) == validKeys.end()) {
                    return false;
                }
            }
            // putAll
            for (const auto& entry : updatedEmployeeInfo) {
                (*it->second)[entry.first] = entry.second;
            }
            return true;
        }
    }

    Object getEmployee(int employeeId) const {
        auto it = employees.find(employeeId);
        if (it == employees.end()) {
            return Object(false);  // Java: Boolean FALSE returned as Object
        } else {
            return Object(it->second);  // live reference to the stored map
        }
    }

    std::map<int, std::shared_ptr<EmployeeInfo>> listEmployees() const {
        std::map<int, std::shared_ptr<EmployeeInfo>> employeeData;
        for (const auto& entry : employees) {
            auto employeeInfo =
                std::make_shared<EmployeeInfo>(*entry.second);  // shallow copy
            (*employeeInfo)["employee_ID"] = entry.first;
            employeeData.emplace(entry.first, std::move(employeeInfo));
        }
        return employeeData;
    }
};

}  // namespace org::example