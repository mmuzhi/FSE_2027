from typing import Dict, Optional, Union


class HRManagementSystem:
    def __init__(self) -> None:
        self.employees: Dict[int, Dict[str, Union[str, int]]] = {}

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

    def update_employee(self, employee_id: int, employee_info: Dict[str, Union[str, int]]) -> bool:
        if employee_id not in self.employees:
            return False

        employee = self.employees[employee_id]

        # Validate all keys first (no partial updates on failure), mirroring the C++ two-pass logic.
        for key in employee_info:
            if key not in employee:
                return False

        for key, value in employee_info.items():
            employee[key] = value

        return True

    def get_employee(self, employee_id: int) -> Optional[Dict[str, Union[str, int]]]:
        if employee_id in self.employees:
            # C++ returns the map by value; return a copy so caller mutations
            # cannot affect internal state.
            return dict(self.employees[employee_id])
        return None

    def list_employees(self) -> Dict[int, Dict[str, Union[str, int]]]:
        employee_data: Dict[int, Dict[str, Union[str, int]]] = {}

        for employee_id, employee_info in self.employees.items():
            employee_details: Dict[str, Union[str, int]] = {"employee_ID": employee_id}
            employee_details.update(employee_info)
            employee_data[employee_id] = employee_details

        return employee_data