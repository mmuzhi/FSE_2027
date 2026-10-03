#include <unordered_map>
#include <string>
#include <optional>
#include <set>
#include <variant>
#include <any>
#include <iostream>
#include <set>

struct Employee {
    std::string name;
    std::string position;
    std::string department;
    int salary;
};

class HRManagementSystem {
private:
    std::unordered_map<int, Employee> employees;

    // Helper function to validate employee_info keys
    bool validateEmployeeInfo(const std::unordered_map<std::string, std::any>& employee_info) {
        static const std::set<std::string> allowed_keys = {"name", "position", "department", "salary"};
        for (const auto& kv : employee_info) {
            if (allowed_keys.find(kv.first) == allowed_keys.end()) {
                return false;
            }
        }
        return true;
    }

public:
    HRManagementSystem() = default;

    bool add_employee(int employee_id, const std::string& name, const std::string& position, 
                     const std::string& department, int salary) {
        if (employees.find(employee_id) != employees.end()) {
            return false;
        }
        employees[employee_id] = {name, position, department, salary};
        return true;
    }

    bool remove_employee(int employee_id) {
        if (employees.find(employee_id) != employees.end()) {
            employees.erase(employee_id);
            return true;
        }
        return false;
    }

    bool update_employee(int employee_id, const std::unordered_map<std::string, std::any>& employee_info) {
        if (!validateEmployeeInfo(employee_info)) {
            return false;
        }
        auto it = employees.find(employee_id);
        if (it == employees.end()) {
            return false;
        }
        auto& emp = it->second;
        for (const auto& kv : employee_info) {
            if (kv.first == "name") {
                emp.name = std::any_cast<std::string>(kv.second);
            } else if (kv.first == "position") {
                emp.position = std::any_cast<std::string>(kv.second);
            } else if (kv.first == "department") {
                emp.department = std::any_cast<std::string>(kv.second);
            } else if (kv.first == "salary") {
                emp.salary = std::any_cast<int>(kv.second);
            }
        }
        return true;
    }

    std::optional<Employee> get_employee(int employee_id) {
        auto it = employees.find(employee_id);
        if (it != employees.end()) {
            return it->second;
        }
        return std::nullopt;
    }

    std::unordered_map<int, Employee> list_employees() {
        std::unordered_map<int, Employee> result;
        for (const auto& kv : employees) {
            result[kv.first] = kv.second;
        }
        return result;
    }
};