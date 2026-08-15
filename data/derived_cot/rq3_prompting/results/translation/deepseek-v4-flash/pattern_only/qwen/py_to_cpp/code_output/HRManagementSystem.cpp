#include <map>
#include <string>
#include <variant>
#include <utility>

using Employee = std::map<std::string, std::variant<std::string, int>>;

class HRManagementSystem {
public:
    std::map<int, Employee> employees;

    bool add_employee(int employee_id, const std::string& name, const std::string& position, const std::string& department, int salary) {
        if (employees.find(employee_id) != employees.end()) {
            return false;
        }
        Employee emp;
        emp["name"] = name;
        emp["position"] = position;
        emp["department"] = department;
        emp["salary"] = salary;
        employees[employee_id] = std::move(emp);
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
        Employee* employee = get_employee(employee_id);
        if (employee == nullptr) {
            return false;
        }
        for (const auto& [key, value] : employee_info) {
            if (employee->find(key) == employee->end()) {
                return false;
            }
        }
        for (const auto& [key, value] : employee_info) {
            (*employee)[key] = value;
        }
        return true;
    }

    Employee* get_employee(int employee_id) {
        auto it = employees.find(employee_id);
        if (it == employees.end()) {
            return nullptr;
        }
        return &it->second;
    }

    const Employee* get_employee(int employee_id) const {
        auto it = employees.find(employee_id);
        if (it == employees.end()) {
            return nullptr;
        }
        return &it->second;
    }

    std::map<int, Employee> list_employees() const {
        std::map<int, Employee> employee_data;
        for (const auto& [employee_id, employee_info] : employees) {
            Employee employee_details = employee_info;
            employee_details["employee_ID"] = employee_id;
            employee_data[employee_id] = std::move(employee_details);
        }
        return employee_data;
    }
};