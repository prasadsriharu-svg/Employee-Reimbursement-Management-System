"""expenses = {"Travel":2200, "Food":750, "Accommodation":3500, "Stationery":150}

total_expenses = 0

for category, amount in expenses.items():
    total_expenses += amount
    print(f"Expense category: {category}, Amount: {amount}")

print(f"Total expenses: {total_expenses}")
print(f"Total expenses using sum(): {sum(expenses.values())}")


claim = {
    "employee": "Hari",
    "category": "Travel",
    "amount": 2200,
    "status": "Submitted"
}
claim["receipt"] = "travel_receipt.pdf"

print("After adding receipt:")
for key, value in claim.items():
    print(f"{key}:{value}")

claim.pop("receipt")

print("After removing receipt:")
for key, value in claim.items():
    print(f"{key}:{value}")
"""
#Using multiple dictionaties

claims = [{
        "employee": "Hari",
        "category": "Travel",
        "amount": 2200,
        "status": "Submitted"
        },
       {"employee": "Priya",
            "category": "Food",
            "amount": 750,
            "status": "Approved"
        }]

for claim in claims:
    print(f"Employee:{claim['employee']}, category:{claim['category']}, amount:{claim['amount']}, status:{claim['status']}")

"""
Output:
PS C:\Projects\New\ReimbursementManagementSystem> python .\dictionaries.py
Employee:Hari, category:Travel, amount:2200, status:Submitted
Employee:Priya, category:Food, amount:750, status:Approved
"""
