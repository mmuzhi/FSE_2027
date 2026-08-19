class HRManagementSystem:
    def __init__(self):
        self.employees = {}

    def add_employee(self, employee_id, name, position, department, salary):
        if employee_id in self.employees:
            return False
        self.employees[employee_id] = {
            "name": name,
            "position": position,
            "department": department,
            "salary": salary,
        }
        return True

    def remove_employee(self, employee_id):
        if employee_id in self.employees:
            del self.employees[employee_id]
            return True
        return False

    def update_employee(self, employee_id, employee_info):
        if employee_id not in self.employees:
            return False
        employee = self.employees[employee_id]
        # Validation pass first: C++ checks all keys before applying any update
        for key in employee_info:
            if key not in employee:
                return False
        for key, value in employee_info.items():
            employee[key] = value
        return True

    def get_employee(self, employee_id):
        # Returns a copy (C++ returns by value), None for std::nullopt
        if employee_id in self.employees:
            return dict(self.employees[employee_id])
        return None

    def list_employees(self):
        employee_data = {}
        for employee_id, employee_info in self.employees.items():
            employee_details = {"employee_ID": employee_id}
            for key, value in employee_info.items():
                employee_details[key] = value
            employee_data[employee_id] = employee_details
        return employee_data