# Hierarchical Inheritance Example
class Employee:    # Base Parent Class
    def login(self):
        return "User logged into internal server."
class Manager(Employee):  # Child Class 1
    def approve_leaves(self):
        return "Approving employee vacation requests."
class Developer(Employee):  # Child Class 2
    def write_code(self):
        return "Compiling code and fixing bugs."
tech_manager = Manager()    # Both classes share 'login', but have unique internal features
software_dev = Developer()
print(tech_manager.login())  # Shared method
print(software_dev.login())  # Shared method