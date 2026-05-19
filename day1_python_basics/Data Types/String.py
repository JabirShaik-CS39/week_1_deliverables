# Reverse a String
var = str(input("Enter a string: "))
rev_var = var[::-1]
print("Reversed string:", rev_var)

# Length of a String
length = len(var)   
print( length)

# Check Palindrome 
if var == var[::-1]:
    print("Palindrome")
else:
    print("Not Palindrome");


