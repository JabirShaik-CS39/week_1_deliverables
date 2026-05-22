# Multi-level Inheritance Example

class ElectronicDevice:   # Grandparent Class
    def power_on(self):
        return "Powering up system..."
class Computer(ElectronicDevice):  # Parent Class inheriting from ElectronicDevice
    def boot_os(self):
        return "Loading Operating System..."
class Laptop(Computer):    # Child Class inheriting from Computer
    def close_lid(self):
        return "Going into sleep mode."
my_laptop = Laptop()
print(my_laptop.power_on())  # From Grandparent
print(my_laptop.boot_os())   # From Parent
print(my_laptop.close_lid())  # From Child