# Logical conditions in Python
age = 20
citizen = True

if age >= 18:
    if citizen:
        print("Eligible to vote")

# Using logical operators
if age >= 18 and citizen:
    print("Eligible to vote")

# Using 'or' operator
has_id = True
if age >= 18 or has_id:
    print("Eligible to vote or has ID")
    
# Using 'not' operator
is_student = False
if not is_student:
    print("Not a student")
