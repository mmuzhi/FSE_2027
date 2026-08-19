#include <map>
#include <string>
#include <variant>

class HRManagementSystem {
public:
    using Value = std::variant<int, std::string>;
    using EmployeeInfo = std::map<std::string, Value>;

    HRManagementSystem() = default;

    bool add_employee(int employee_id, const std::string& name,
                      const std::string& position, const std::string& department,
                      int salary) {
        if (employees.find(employee_id) != employees.end()) {
            return false;
        }
        employees[employee_id] = EmployeeInfo{
            {"name", name},
            {"position", position},
            {"department", department},
            {"salary", salary}
        };
        return true;
    }

    bool remove_employee(int employee_id) {
        auto it = employees.find(employee_id);
        if (it != employees.end()) {
            employees.erase(it);
            return true;
        }
        return false;
    }

    bool update_employee(int employee_id, const EmployeeInfo& employee_info) {
        // Python returns the live dict from get_employee; a pointer preserves
        // that aliasing so mutations below affect the stored employee.
        EmployeeInfo* employee = get_employee(employee_id);
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

    // Returns a pointer to the live record (mutable, like Python's reference),
    // or nullptr when absent (Python returns False).
    EmployeeInfo* get_employee(int employee_id) {
        auto it = employees.find(employee_id);
        if (it != employees.end()) {
            return &it->second;
        }
        return nullptr;
    }

    std::map<int, EmployeeInfo> list_employees() const {
        std::map<int, EmployeeInfo> employee_data;
        for (const auto& [employee_id, employee_info] : employees) {
            EmployeeInfo employee_details;
            employee_details["employee_ID"] = employee_id;
            for (const auto& [key, value] : employee_info) {
                employee_details[key] = value;
            }
            employee_data[employee_id] = employee_details;
        }
        return employee_data;
    }

    std::map<int, EmployeeInfo> employees;
};