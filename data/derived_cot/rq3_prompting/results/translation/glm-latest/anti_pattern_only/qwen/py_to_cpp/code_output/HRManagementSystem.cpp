#include <map>
#include <optional>
#include <string>
#include <utility>
#include <variant>

// ---------------------------------------------------------------------------
// HRManagementSystem: a personnel management system that supports adding,
// deleting, querying and updating employees.
//
// Type mapping used for the translation (C++17):
//   employee record dict        -> EmployeeInfo  (std::map<std::string, EmployeeValue>)
//   record values (str / int)   -> EmployeeValue (std::variant<std::string, long long>)
//   self.employees              -> EmployeeMap   (std::map<int, EmployeeInfo>)
//   Python "False" from get_employee -> std::nullopt
// ---------------------------------------------------------------------------

using EmployeeValue = std::variant<std::string, long long>;
using EmployeeInfo  = std::map<std::string, EmployeeValue>;
using EmployeeMap   = std::map<int, EmployeeInfo>;

class HRManagementSystem {
public:
    // Public, mirroring the freely accessible Python attribute self.employees.
    EmployeeMap employees;

    // Add a new employee to the HRManagementSystem.
    // Returns false if an employee with this id already exists,
    // otherwise stores the employee and returns true.
    bool add_employee(int employee_id, const std::string& name,
                      const std::string& position, const std::string& department,
                      long long salary) {
        if (employees.find(employee_id) != employees.end()) {
            return false;
        }
        employees[employee_id] = EmployeeInfo{
            {"name",      name},
            {"position",  position},
            {"department", department},
            {"salary",    salary},
        };
        return true;
    }

    // Remove an employee from the HRManagementSystem.
    // Returns true if the employee existed (and was removed), false otherwise.
    bool remove_employee(int employee_id) {
        auto it = employees.find(employee_id);
        if (it != employees.end()) {
            employees.erase(it);
            return true;
        }
        return false;
    }

    // Update an employee's information in the HRManagementSystem.
    // Returns false if the employee does not exist, or if employee_info
    // contains any key that is not already part of the employee's record
    // (the update is all-or-nothing: nothing is written in that case).
    // On success every given key/value is written into the stored record.
    bool update_employee(int employee_id, const EmployeeInfo& employee_info) {
        // Python: employee = self.get_employee(employee_id)
        //         if employee == False: return False
        auto it = employees.find(employee_id);
        if (it == employees.end()) {
            return false;
        }
        EmployeeInfo& employee = it->second;  // reference to the stored record

        // First pass: every key must already exist in the record.
        for (const auto& entry : employee_info) {
            if (employee.find(entry.first) == employee.end()) {
                return false;
            }
        }
        // Second pass: apply the updates through the reference, exactly like
        // the Python code mutates the dict returned by get_employee().
        for (const auto& entry : employee_info) {
            employee[entry.first] = entry.second;
        }
        return true;
    }

    // Get an employee's information from the HRManagementSystem.
    // Returns the employee's record if present, std::nullopt otherwise
    // (std::nullopt plays the role of Python's False).
    std::optional<EmployeeInfo> get_employee(int employee_id) const {
        auto it = employees.find(employee_id);
        if (it != employees.end()) {
            return it->second;
        }
        return std::nullopt;
    }

    // List all employees' information in the HRManagementSystem.
    // Returns a map of employee_id -> record, where each record is a copy of
    // the stored one, augmented with the key "employee_ID" holding the id.
    EmployeeMap list_employees() const {
        EmployeeMap employee_data;
        for (const auto& [employee_id, employee_info] : employees) {
            EmployeeInfo employee_details;
            employee_details["employee_ID"] = employee_id;
            for (const auto& [key, value] : employee_info) {
                employee_details[key] = value;
            }
            employee_data[employee_id] = std::move(employee_details);
        }
        return employee_data;
    }
};