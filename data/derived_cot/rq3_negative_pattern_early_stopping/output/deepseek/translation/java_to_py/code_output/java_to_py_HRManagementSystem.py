class HRManagementSystem:
    def __init__(self):
        self.employees = {}  # int -> dict

    def addEmployee(self, employee_id, name, position, department, salary):
        if employee_id in self.employees:
            return False
        employee_info = {
            "name": name,
            "position": position,
            "department": department,
            "salary": salary
        }
        self.employees[employee_id] = employee_info
        return True

    def removeEmployee(self, employee_id):
        if employee_id in self.employees:
            del self.employees[employee_id]
            return True
        return False

    def updateEmployee(self, employee_id, updated_employee_info):
        employee_info = self.employees.get(employee_id)
        if employee_info is None:
            return False

        valid_keys = {"name", "position", "department", "salary"}
        for key in updated_employee_info:
            if key not in valid_keys:
                return False

        employee_info.update(updated_employee_info)
        return True

    def getEmployee(self, employee_id):
        employee_info = self.employees.get(employee_id)
        if employee_info is None:
            return False
        return employee_info

    def listEmployees(self):
        employee_data = {}
        for emp_id, emp_info in self.employees.items():
            copied_info = emp_info.copy()
            copied_info["employee_ID"] = emp_id
            employee_data[emp_id] = copied_info
        return employee_data