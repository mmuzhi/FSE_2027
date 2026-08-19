#include <functional>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <variant>

namespace org::example {

class HRManagementSystem {
public:
    // Java "Object" values here are Boolean, Integer, Double, or String.
    using Object = std::variant<bool, int, double, std::string>;
    using EmployeeInfo = std::unordered_map<std::string, Object>;

    std::unordered_map<int, EmployeeInfo> employees;

    HRManagementSystem() = default;

    bool addEmployee(int employeeId, const std::string& name, const std::string& position,
                     const std::string& department, double salary) {
        if (employees.find(employeeId) != employees.end()) {
            return false;
        }
        EmployeeInfo employeeInfo;
        employeeInfo["name"] = name;
        employeeInfo["position"] = position;
        employeeInfo["department"] = department;
        employeeInfo["salary"] = salary;
        employees.emplace(employeeId, std::move(employeeInfo));
        return true;
    }

    bool removeEmployee(int employeeId) {
        if (employees.find(employeeId) != employees.end()) {
            employees.erase(employeeId);
            return true;
        }
        return false;
    }

    bool updateEmployee(int employeeId, const EmployeeInfo& updatedEmployeeInfo) {
        auto it = employees.find(employeeId);
        if (it == employees.end()) {
            return false;
        }
        static const std::unordered_set<std::string> validKeys = {"name", "position", "department", "salary"};
        for (const auto& entry : updatedEmployeeInfo) {
            if (validKeys.find(entry.first) == validKeys.end()) {
                return false;
            }
        }
        EmployeeInfo& employeeInfo = it->second;
        // Java's putAll overwrites existing keys; insert_or_assign matches that.
        for (const auto& entry : updatedEmployeeInfo) {
            employeeInfo.insert_or_assign(entry.first, entry.second);
        }
        return true;
    }

    // Returns Boolean false if absent, otherwise a live reference to the stored map
    // (mutations through it affect internal state, as in Java).
    std::variant<bool, std::reference_wrapper<EmployeeInfo>> getEmployee(int employeeId) {
        auto it = employees.find(employeeId);
        if (it == employees.end()) {
            return false;
        }
        return std::ref(it->second);
    }

    std::unordered_map<int, EmployeeInfo> listEmployees() const {
        std::unordered_map<int, EmployeeInfo> employeeData;
        for (const auto& entry : employees) {
            EmployeeInfo employeeInfo = entry.second; // defensive copy, as in Java
            employeeInfo["employee_ID"] = entry.first;
            employeeData.emplace(entry.first, std::move(employeeInfo));
        }
        return employeeData;
    }
};

} // namespace org::example