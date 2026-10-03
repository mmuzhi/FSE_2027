#include <map>
#include <string>
#include <variant>

class HRManagementSystem {
public:
    using Value = std::variant<int, std::string>;
    using EmployeeInfo = std::map<std::string, Value>;
    using GetEmployeeResult = std::variant<EmployeeInfo*, bool>;
    using ConstGetEmployeeResult = std::variant<const EmployeeInfo*, bool>;

private:
    std::map<int, EmployeeInfo> employees;

public:
    HRManagementSystem() = default;

    bool add_employee(int employee_id, const std::string& name, const std::string& position, const std::string& department, int salary) {
        if (employees.find(employee_id) != employees.end()) {
            return false;
        }
        employees[employee_id] = {
            {"name", name},
            {"position", position},
            {"department", department},
            {"salary", salary}
        };
        return true;
    }

    bool remove_employee(int employee_id) {
        if (employees.find(employee_id) != employees.end()) {
            employees.erase(employee_id);
            return true;
        }
        return false;
    }

    bool update_employee(int employee_id, const EmployeeInfo& employee_info) {
        GetEmployeeResult emp_result = get_employee(employee_id);
        if (emp_result == GetEmployeeResult(false)) {
            return false;
        }
        EmployeeInfo* employee = std::get<EmployeeInfo*>(emp_result);
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

    GetEmployeeResult get_employee(int employee_id) {
        auto it = employees.find(employee_id);
        if (it != employees.end()) {
            return &(it->second);
        }
        return false;
    }

    ConstGetEmployeeResult get_employee(int employee_id) const {
        auto it = employees.find(employee_id);
        if (it != employees.end()) {
            return &(it->second);
        }
        return false;
    }

    std::map<int, EmployeeInfo> list_employees() const {
        std::map<int, EmployeeInfo> employee_data;
        if (!employees.empty()) {
            for (const auto& [employee_id, employee_info] : employees) {
                EmployeeInfo employee_details;
                employee_details["employee_ID"] = employee_id;
                for (const auto& [key, value] : employee_info) {
                    employee_details[key] = value;
                }
                employee_data[employee_id] = employee_details;
            }
        }
        return employee_data;
    }
};