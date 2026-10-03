#include <string>
#include <unordered_map>
#include <map>
#include <variant>
#include <vector>

class HRManagementSystem {
private:
    // Employee data stored as map of fields: name (string), position (string), department (string), salary (int)
    using EmployeeInfo = std::map<std::string, std::variant<std::string, int>>;
    std::unordered_map<int, EmployeeInfo> employees;

public:
    HRManagementSystem() {}

    bool add_employee(int employee_id, const std::string& name, const std::string& position,
                      const std::string& department, int salary) {
        if (employees.find(employee_id) != employees.end()) {
            return false;
        }
        EmployeeInfo info;
        info["name"] = name;
        info["position"] = position;
        info["department"] = department;
        info["salary"] = salary;
        employees[employee_id] = info;
        return true;
    }

    bool remove_employee(int employee_id) {
        auto it = employees.find(employee_id);
        if (it == employees.end()) {
            return false;
        }
        employees.erase(it);
        return true;
    }

    bool update_employee(int employee_id, const std::map<std::string, std::variant<std::string, int>>& employee_info) {
        auto it = employees.find(employee_id);
        if (it == employees.end()) {
            return false;
        }
        EmployeeInfo& emp = it->second;
        for (const auto& [key, value] : employee_info) {
            if (emp.find(key) == emp.end()) {
                return false;
            }
        }
        for (const auto& [key, value] : employee_info) {
            emp[key] = value;
        }
        return true;
    }

    // Returns a pointer to the employee info if exists, nullptr otherwise.
    // To mimic Python's return of False (boolean) we use nullptr for failure.
    const EmployeeInfo* get_employee(int employee_id) const {
        auto it = employees.find(employee_id);
        if (it == employees.end()) {
            return nullptr;
        }
        return &(it->second);
    }

    // Non-const version for modification (like Python's direct reference)
    EmployeeInfo* get_employee(int employee_id) {
        auto it = employees.find(employee_id);
        if (it == employees.end()) {
            return nullptr;
        }
        return &(it->second);
    }

    std::map<int, std::map<std::string, std::variant<std::string, int>>> list_employees() const {
        std::map<int, std::map<std::string, std::variant<std::string, int>>> result;
        for (const auto& [id, info] : employees) {
            std::map<std::string, std::variant<std::string, int>> details;
            details["employee_ID"] = id;
            for (const auto& [key, value] : info) {
                details[key] = value;
            }
            result[id] = details;
        }
        return result;
    }
};