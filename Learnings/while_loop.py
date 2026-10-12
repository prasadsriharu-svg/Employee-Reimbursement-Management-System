claim_number = 1

while claim_number <=5:
    #print(f"processing claim number: {claim_number}")
    if claim_number == 3:
        print(f"Claim number {claim_number} skipping processing")
        claim_number +=1
        continue
        #break
    
    print(f"processing claim number: {claim_number}")
    claim_number +=1