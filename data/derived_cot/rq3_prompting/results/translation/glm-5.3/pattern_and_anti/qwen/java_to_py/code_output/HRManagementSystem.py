class HRManagementSystem:
    def __init__(self):
        self.employees = {}

    def add_employee(self, employee_id, name, position, department, salary):
        if employee_id in self.employees:
            return False
        else:
            employee_info = {
                "name": name,
                "position": position,
                "department": department,
                "salary": salary,
            }
            self.employees[employee_id] = employee_info
            return True

    def remove_employee(self, employee_id):
        if employee_id in self.employees:
            del self.employees[employee_id]
            return True
        else:
            return False

    def update_employee(self, employee_id, updated_employee_info):
        employee_info = self.employees.get(employee_id)
        if employee_info is None:
            return False
        else:
            valid_keys = {"name", "position", "department", "salary"}
            for key in updated_employee_info:
                if key not in valid_keys:
                    return False
            employee_info.update(updated_employee_info)
            return True

    def get_employee(self, employee_id):
        employee_info = self.employees.get(employee_id)
        if employee_info is None:
            return False
        else:
            return employee_info

    def list_employees(self):
        employee_data = {}
        for employee_id, employee_info in self.employees.items():
            copied_info = dict(employee_info)
            copied_info["employee_ID"] = employee_id
            employee_data[employee_id] = copied_info
        return employee_data