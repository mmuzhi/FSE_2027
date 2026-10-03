class HRManagementSystem:
    def __init__(self):
        self.employees = {}

    def addEmployee(self, employeeId, name, position, department, salary):
        if employeeId in self.employees:
            return False
        else:
            employeeInfo = {
                "name": name,
                "position": position,
                "department": department,
                "salary": salary,
            }
            self.employees[employeeId] = employeeInfo
            return True

    def removeEmployee(self, employeeId):
        if employeeId in self.employees:
            del self.employees[employeeId]
            return True
        else:
            return False

    def updateEmployee(self, employeeId, updatedEmployeeInfo):
        employeeInfo = self.employees.get(employeeId)
        if employeeInfo is None:
            return False
        else:
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
        else:
            return employeeInfo

    def listEmployees(self):
        employeeData = {}
        for employeeId, employeeInfo in self.employees.items():
            newEmployeeInfo = dict(employeeInfo)
            newEmployeeInfo["employee_ID"] = employeeId
            employeeData[employeeId] = newEmployeeInfo
        return employeeData