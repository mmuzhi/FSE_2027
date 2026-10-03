#include <unordered_map>
#include <unordered_set>
#include <string>
#include <any>

class HRManagementSystem {
public:
    std::unordered_map<int, std::unordered_map<std::string, std::any>> employees;

    HRManagementSystem() = default;

    bool addEmployee(int employeeId, const std::string& name, const std::string& position, const std::string& department, double salary) {
        if (employees.find(employeeId) != employees.end()) {
            return false;
        } else {
            std::unordered_map<std::string, std::any> employeeInfo;
            employeeInfo["name"] = name;
            employeeInfo["position"] = position;
            employeeInfo["department"] = department;
            employeeInfo["salary"] = salary;
            employees[employeeId] = std::move(employeeInfo);
            return true;
        }
    }

    bool removeEmployee(int employeeId) {
        if (employees.find(employeeId) != employees.end()) {
            employees.erase(employeeId);
            return true;
        } else {
            return false;
        }
    }

    bool updateEmployee(int employeeId, const std::unordered_map<std::string, std::any>& updatedEmployeeInfo) {
        auto it = employees.find(employeeId);
        if (it == employees.end()) {
            return false;
        } else {
            static const std::unordered_set<std::string> validKeys = {"name", "position", "department", "salary"};
            for (const auto& pair : updatedEmployeeInfo) {
                if (validKeys.find(pair.first) == validKeys.end()) {
                    return false;
                }
            }
            for (const auto& pair : updatedEmployeeInfo) {
                it->second[pair.first] = pair.second;
            }
            return true;
        }
    }

    std::any getEmployee(int employeeId) {
        auto it = employees.find(employeeId);
        if (it == employees.end()) {
            return false;
        } else {
            return &it->second;
        }
    }

    std::unordered_map<int, std::unordered_map<std::string, std::any>> listEmployees() {
        std::unordered_map<int, std::unordered_map<std::string, std::any>> employeeData;
        for (const auto& entry : employees) {
            int employeeId = entry.first;
            std::unordered_map<std::string, std::any> employeeInfo = entry.second;
            employeeInfo["employee_ID"] = employeeId;
            employeeData[employeeId] = std::move(employeeInfo);
        }
        return employeeData;
    }
};