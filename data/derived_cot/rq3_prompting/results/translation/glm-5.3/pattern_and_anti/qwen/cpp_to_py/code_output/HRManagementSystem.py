from typing import Dict, Optional, Union

EmployeeInfo = Dict[str, Union[str, int]]


class HRManagementSystem:
    def __init__(self) -> None:
        self.employees: Dict[int, EmployeeInfo] = {}

    def add_employee(self, employee_id: int, name: str, position: str, department: str, salary: int) -> bool:
        if employee_id in self.employees:
            return False
        self.employees[employee_id] = {
            "name": name,
            "position": position,
            "department": department,
            "salary": salary,
        }
        return True

    def remove_employee(self, employee_id: int) -> bool:
        if employee_id in self.employees:
            del self.employees[employee_id]
            return True
        return False

    def update_employee(self, employee_id: int, employee_info: EmployeeInfo) -> bool:
        employee = self.employees.get(employee_id)
        if employee is None:
            return False

        for key in employee_info:
            if key not in employee:
                return False

        for key, value in employee_info.items():
            employee[key] = value

        return True

    def get_employee(self, employee_id: int) -> Optional[EmployeeInfo]:
        employee = self.employees.get(employee_id)
        if employee is not None:
            return dict(employee)
        return None

    def list_employees(self) -> Dict[int, EmployeeInfo]:
        employee_data: Dict[int, EmployeeInfo] = {}
        for employee_id, employee_info in self.employees.items():
            employee_details: EmployeeInfo = {"employee_ID": employee_id}
            for key, value in employee_info.items():
                employee_details[key] = value
            employee_data[employee_id] = employee_details
        return employee_data