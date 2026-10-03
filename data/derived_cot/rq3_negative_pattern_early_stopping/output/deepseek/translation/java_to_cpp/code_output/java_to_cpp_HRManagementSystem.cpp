#include <unordered_map>
#include <string>
#include <any>
#include <set>

class HRManagementSystem {
public:
    std::unordered_map<int, std::unordered_map<std::string, std::any>> employees;

    HRManagementSystem() = default;

    bool addEmployee(int employeeId, const std::string& name, const std::string& position,
                     const std::string& department, double salary) {
        if (employees.find(employeeId) != employees.end()) {
            return false;
        }
        std::unordered_map<std::string, std::any> employeeInfo;
        employeeInfo["name"] = name;
        employeeInfo["position"] = position;
        employeeInfo["department"] = department;
        employeeInfo["salary"] = salary;
        employees[employeeId] = std::move(employeeInfo);
        return true;
    }

    bool removeEmployee(int employeeId) {
        if (employees.find(employeeId) != employees.end()) {
            employees.erase(employeeId);
            return true;
        }
        return false;
    }

    bool updateEmployee(int employeeId, const std::unordered_map<std::string, std::any>& updatedEmployeeInfo) {
        auto it = employees.find(employeeId);
        if (it == employees.end()) {
            return false;
        }
        static const std::set<std::string> validKeys = {"name", "position", "department", "salary"};
        for (const auto& [key, value] : updatedEmployeeInfo) {
            if (validKeys.find(key) == validKeys.end()) {
                return false;
            }
        }
        for (const auto& [key, value] : updatedEmployeeInfo) {
            it->second[key] = value;
        }
        return true;
    }

    std::any getEmployee(int employeeId) {
        auto it = employees.find(employeeId);
        if (it == employees.end()) {
            return std::any(false);
        }
        return std::any(it->second);
    }

    std::unordered_map<int, std::unordered_map<std::string, std::any>> listEmployees() {
        std::unordered_map<int, std::unordered_map<std::string, std::any>> employeeData;
        for (const auto& [employeeId, employeeInfo] : employees) {
            std::unordered_map<std::string, std::any> info(employeeInfo);
            info["employee_ID"] = employeeId;
            employeeData[employeeId] = std::move(info);
        }
        return employeeData;
    }
};