from typing import Dict, Optional, Union, Any


class HRManagementSystem:
    def __init__(self) -> None:
        self.employees: Dict[int, Dict[str, Union[str, int]]] = {}

    def add_employee(
        self,
        employee_id: int,
        name: str,
        position: str,
        department: str,
        salary: int,
    ) -> bool:
        """
        Adds a new employee. Returns True if added, False if already exists.
        """
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
        """
        Removes an employee by ID. Returns True if removed, False if not found.
        """
        if employee_id in self.employees:
            del self.employees[employee_id]
            return True
        return False

    def update_employee(
        self,
        employee_id: int,
        employee_info: Dict[str, Union[str, int]],
    ) -> bool:
        """
        Updates employee fields. The keys in employee_info must exist already.
        Returns True on success, False if employee not found or any key is invalid.
        """
        if employee_id not in self.employees:
            return False

        for key in employee_info:
            if key not in self.employees[employee_id]:
                return False

        for key, value in employee_info.items():
            self.employees[employee_id][key] = value
        return True

    def get_employee(
        self, employee_id: int
    ) -> Optional[Dict[str, Union[str, int]]]:
        """
        Returns a copy of the employee data if found, else None.
        """
        if employee_id in self.employees:
            return self.employees[employee_id].copy()
        return None

    def list_employees(self) -> Dict[int, Dict[str, Union[str, int]]]:
        """
        Returns a dict of all employees, each entry augmented with "employee_ID".
        """
        result: Dict[int, Dict[str, Union[str, int]]] = {}
        for emp_id, info in self.employees.items():
            emp_copy = info.copy()
            emp_copy["employee_ID"] = emp_id
            result[emp_id] = emp_copy
        return result