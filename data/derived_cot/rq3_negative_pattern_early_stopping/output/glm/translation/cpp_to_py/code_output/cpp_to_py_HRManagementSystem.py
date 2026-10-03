from typing import Optional, Dict, Union


class HRManagementSystem:
    def __init__(self):
        self.employees: Dict[int, Dict[str, Union[str, int]]] = {}

    def add_employee(self, employee_id: int, name: str, position: str, department: str, salary: int) -> bool:
        if employee_id in self.employees:
            return False
        else:
            self.employees[employee_id] = {
                "name": name,
                "position": position,
                "department": department,
                "salary": salary
            }
            return True

    def remove_employee(self, employee_id: int) -> bool:
        if employee_id in self.employees:
            del self.employees[employee_id]
            return True
        else:
            return False

    def update_employee(self, employee_id: int, employee_info: Dict[str, Union[str, int]]) -> bool:
        if employee_id not in self.employees:
            return False

        for key in employee_info:
            if key not in self.employees[employee_id]:
                return False

        for key, value in employee_info.items():
            self.employees[employee_id][key] = value

        return True

    def get_employee(self, employee_id: int) -> Optional[Dict[str, Union[str, int]]]:
        if employee_id in self.employees:
            return dict(self.employees[employee_id])
        return None

    def list_employees(self) -> Dict[int, Dict[str, Union[str, int]]]:
        employee_data = {}

        for employee_id, employee_info in self.employees.items():
            employee_details = {"employee_ID": employee_id}
            for key, value in employee_info.items():
                employee_details[key] = value
            employee_data[employee_id] = employee_details

        return employee_data