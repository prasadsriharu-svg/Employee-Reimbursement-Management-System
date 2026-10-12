total_expenses = 0
expenses =  [1000, 2000, 3000]

for expense in expenses:
    #print(f"Current total expenses: {total_expenses}")
    total_expenses = total_expenses + expense
    if expense == expenses[1]:
        print(f"Total expenses during second iteration: {total_expenses}")
    #print(f"Current expense: {expense}, Total expenses so far: {total_expenses}")

#print(f"Total expenses during second iteration: {total_expenses}")

