#include <unordered_map>
#include <string>
#include <any>
#include <set>
#include <map>
#include <variant>
#include <optional>

using EmployeeMap = std::unordered_map<std::string, std::any>;
using EmployeeMapVariant = std::variant<bool, EmployeeMap>;

class HRManagementSystem {
private:
    std::unordered_map<int, EmployeeMap> employees;

public:
    HRManagementSystem() = default;

    bool addEmployee(int employeeId, const std::string& name, const std::string& position, const std::string& department, double salary) {
        if (employees.find(employeeId) != employees.end()) {
            return false;
        }
        EmployeeMap employeeInfo;
        employeeInfo["name"] = name;
        employeeInfo["position"] = position;
        employeeInfo["department"] = department;
        employeeInfo["salary"] = salary;
        employees[employeeId] = std::move(employeeInfo);
        return true;
    }

    bool removeEmployee(int employeeId) {
        auto it = employees.find(employeeId);
        if (it != employees.end()) {
            employees.erase(it);
            return true;
        }
        return false;
    }

    bool updateEmployee(int employeeId, const std::map<std::string, std::any>& updatedEmployeeInfo) {
        auto it = employees.find(employeeId);
        if (it == employees.end()) {
            return false;
        }
        std::set<std::string> validKeys = {"name", "position", "department", "salary"};
        for (const auto& [key, value] : updatedEmployeeInfo) {
            if (validKeys.find(key) == validKeys.end()) {
                return false;
            }
            it->second[key] = value;
        }
        return true;
    }

    EmployeeMapVariant getEmployee(int employeeId) {
        auto it = employees.find(employeeId);
        if (it == employees.end()) {
            return false;
        } else {
            return it->second;
        }
    }

    std::map<int, EmployeeMap> listEmployees() {
        std::map<int, EmployeeMap> employeeData;
        for (const auto& [id, innerMap] : employees) {
            EmployeeMap employeeInfo = innerMap;
            employeeInfo["employee_ID"] = id;
            employeeData[id] = std::move(employeeInfo);
        }
        return employeeData;
    }
};