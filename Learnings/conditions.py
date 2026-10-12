employee_name = input("Enter employee name: ")
claim_amount = float(input("Enter the claim amount: "))

if claim_amount <= 0:
    print("Invalid claim")
elif claim_amount <=5000:
    print("claim amount is with in the limit, Normal approval process")
elif claim_amount <=10000:
    print("Claim exceeds the limit. Send for review, manager review")
else:
    print("Claim exceeds the limit. Send for special review.")
