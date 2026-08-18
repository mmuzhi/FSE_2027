#include <set>
#include <string>
#include <unordered_map>
#include <variant>

namespace org::example {

class HRManagementSystem {
public:
    // Java Map<String, Object>: values are String, Double, or Integer here.
    using Value = std::variant<std::string, double, int>;
    using EmployeeInfo = std::unordered_map<std::string, Value>;

    std::unordered_map<int, EmployeeInfo> employees;

    HRManagementSystem() = default;

    bool addEmployee(int employeeId, const std::string& name, const std::string& position,
                     const std::string& department, double salary) {
        if (employees.find(employeeId) != employees.end()) {
            return false;
        }
        EmployeeInfo employeeInfo;
        employeeInfo.emplace("name", name);
        employeeInfo.emplace("position", position);
        employeeInfo.emplace("department", department);
        employeeInfo.emplace("salary", salary);
        employees.emplace(employeeId, std::move(employeeInfo));
        return true;
    }

    bool removeEmployee(int employeeId) {
        return employees.erase(employeeId) > 0;
    }

    bool updateEmployee(int employeeId, const EmployeeInfo& updatedEmployeeInfo) {
        auto it = employees.find(employeeId);
        if (it == employees.end()) {
            return false;
        }
        static const std::set<std::string> validKeys = {"name", "position", "department", "salary"};
        // Java validates all keys before applying any change; keep that ordering.
        for (const auto& [key, value] : updatedEmployeeInfo) {
            (void)value; // unused in validation pass
            if (validKeys.find(key) == validKeys.end()) {
                return false;
            }
        }
        // putAll semantics: overwrite existing keys.
        for (const auto& [key, value] : updatedEmployeeInfo) {
            it->second[key] = value;
        }
        return true;
    }

    // Java returns Object: Boolean(false) when absent, otherwise the employee map.
    std::variant<bool, EmployeeInfo> getEmployee(int employeeId) {
        auto it = employees.find(employeeId);
        if (it == employees.end()) {
            return false;
        }
        return it->second;
    }

    std::unordered_map<int, EmployeeInfo> listEmployees() {
        std::unordered_map<int, EmployeeInfo> employeeData;
        for (const auto& [employeeId, info] : employees) {
            EmployeeInfo employeeInfo = info; // defensive copy, as in Java
            employeeInfo.emplace("employee_ID", employeeId);
            employeeData.emplace(employeeId, std::move(employeeInfo));
        }
        return employeeData;
    }
};

} // namespace org::example