class Employee:
    def __init__(self, name, role):
        self.name = name
        self.role = role

employee1 = Employee("Hari", "Manager")
print(f"Employee Name: {employee1.name}, Employee Role: {employee1.role}")
"""
Output:
PS C:\Projects\New\ReimbursementManagementSystem> python .\class.py
Employee Name: Hari, Employee Role: Manager
"""