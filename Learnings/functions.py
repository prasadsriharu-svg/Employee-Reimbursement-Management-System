def calculate_total(travel, food, accommodation=0, stationery=0):
    total = travel + food + accommodation + stationery
    return total

total_all = calculate_total(2200, 750, 3500, 300)
print(f"Total reimbursement: {total_all}")
total_few = calculate_total(2200, 750)
print(f"Total reimbursement: {total_few}")