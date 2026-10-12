# Employee Reimbursement Calculator

print("===================================")
print(" EMPLOYEE REIMBURSEMENT CALCULATOR")
print("===================================")

# Get employee details
employee_name = input("Enter employee name: ")

# Get expense details
travel_expense = float(input("Enter travel expense: "))
food_expense = float(input("Enter food expense: "))
accommodation_expense = float(input("Enter accommodation expense: "))
stationery_expense = float(input("Enter stationery expense: "))
miscellaneous_expenses = float(input("Enter miscellaneous expenses: "))

# Calculate total reimbursement
total_reimbursement = (travel_expense + food_expense + accommodation_expense + stationery_expense + miscellaneous_expenses) 

# Display reimbursement summary
print("\n ==============CLAIM SUMMARY================")

print("Employee Name:", employee_name)
print("Travel Expense:", travel_expense)
print("Food Expense:", food_expense)
print("Accommodation Expense:", accommodation_expense)
print("Stationery Expense:", stationery_expense)
print("Miscellaneous Expenses:", miscellaneous_expenses)

print("-----------------------------------")
print("Total Reimbursement:", total_reimbursement)
print("===================================")