# Single Inheritance Example in Python
class Vehicle:  # Parent Class
    def move(self):
        return "Moving across the ground..."
class Car(Vehicle): # Child Class inheriting from Vehicle
    def honk(self):
        return "Beep beep!"
my_car = Car()
print(my_car.move())  # Inherited method
print(my_car.honk())  # Own method