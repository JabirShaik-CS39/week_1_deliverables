# checking the grade based on marks using if-elif-else statements
marks = int(input("Enter your marks: "))

if marks >= 90:
    print("Grade A")
elif marks >= 70:
    print("Grade B")
elif marks >= 50:
    print("Grade C")
else:
    print("Fail")

# checking the day of the week based on user input
day = input("Enter a day of the week: ").lower()
if day == "monday":
    print("It's the start of the week.")
elif day == "friday":
    print("It's almost the weekend.")
elif day == "saturday" or day == "sunday":
    print("It's the weekend!")
else:
    print("It's a regular weekday.")