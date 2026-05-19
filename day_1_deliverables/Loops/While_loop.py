Num = int(input("Enter a number: "))
while Num <= 5:
    print(Num)
    Num += 1

# Infinite loop
for i in range(1, 10):
    if i == 5:
        break

    print(i)

# continue statement
for i in range(1, 6):
    if i == 3:
        continue

    print(i)

# nested loops
for i in range(1, 4):
    for j in range(1, 4):
        print(i, j)


# calculate the factorial of a number using while loop
while True:
    print("\n--- Calculator ---")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exit")
    choice = input("Enter your choice (1-5): ")

    # Exit condition
    if choice == '5':
        print("Calculator closed")
        break

    # Input numbers
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    # Operations
    if choice == '1':
        print("Result:", num1 + num2)

    elif choice == '2':
        print("Result:", num1 - num2)

    elif choice == '3':
        print("Result:", num1 * num2)

    elif choice == '4':

        if num2 != 0:
            print("Result:", num1 / num2)
        else:
            print("Cannot divide by zero")

    else:
        print("Invalid choice")