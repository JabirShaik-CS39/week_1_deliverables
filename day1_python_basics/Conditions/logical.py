# Logical Operators
age = 25
salary = 30000
if age > 18 and salary > 20000:
    print("Loan approved")

# checking the day as a holiday 
day = input("Day: ")
if day == "Sunday" or day == "Saturday":
    print("Holiday")
else:
    print("Working day")

balance = int(input(" Balance: "))
withdraw = int(input(" Withdrawal amount: "))
if withdraw <= balance:
    print("Transaction successful")
else:
    print("Insufficient balance")

