# Code for the Object section of the OOP Architecture lesson
class Dog:
    def __init__(self, name):
        self.name = name  # Attribute
    def bark(self):       # Method
        return f"{self.name} says Woof!"
my_dog = Dog("Buddy")      # 1. Creating the object (Instantiation)
print(my_dog.name)         # 2. Accessing data and actions (Dot Notation)
print(my_dog.bark())    

# A Calculator class without a constructor
class Calculator:
    def add(self, num1, num2):
        return num1 + num2
    def multiply(self, num1, num2):
        return num1 * num2
my_calc = Calculator()                 # 1. Creating an empty object
sum_result = my_calc.add(5, 10)        # 2. Using the methods by passing data directly into them
product_result = my_calc.multiply(4, 3)
print(f"5 + 10 = {sum_result}")       
print(f"4 * 3 = {product_result}")    