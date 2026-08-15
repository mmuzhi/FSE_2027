class HRManagementSystem:
    def __init__(self):
        self.employees = {}

    def addEmployee(self, employeeId, name, position, department, salary):
        if employeeId in self.employees:
            return False
        employeeInfo = {
            "name": name,
            "position": position,
            "department": department,
            "salary": float(salary)
        }
        self.employees[employeeId] = employeeInfo
        return True

    def removeEmployee(self, employeeId):
        if employeeId in self.employees:
            del self.employees[employeeId]
            return True
        return False

    def updateEmployee(self, employeeId, updatedEmployeeInfo):
        employeeInfo = self.employees.get(employeeId)
        if employeeInfo is None:
            return False
        validKeys = {"name", "position", "department", "salary"}
        for key in updatedEmployeeInfo:
            if key not in validKeys:
                return False
        employeeInfo.update(updatedEmployeeInfo)
        return True

    def getEmployee(self, employeeId):
        employeeInfo = self.employees.get(employeeId)
        if employeeInfo is None:
            return False
        return employeeInfo

    def listEmployees(self):
        employeeData = {}
        for employeeId, employeeInfo in self.employees.items():
            employeeInfoCopy = dict(employeeInfo)
            employeeInfoCopy["employee_ID"] = employeeId
            employeeData[employeeId] = employeeInfoCopy
        return employeeData