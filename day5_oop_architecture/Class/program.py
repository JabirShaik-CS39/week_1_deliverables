# code for a simple class representation of a user profile in an application

class UserProfile:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def greet_user(self):
        return f"Welcome back, {self.username}! Role: [{self.role}]"

# Using the Class (Creating an object)
new_user = UserProfile("Alice", "Admin")
print(new_user.greet_user())


# A Product class without a constructor
class Product:
    # No __init__ constructor is written here

    def get_discount_price(self):
        # Calculates the final price after subtracting the discount amount
        final_price = self.price - self.discount
        return f"The final price for {self.name} is ${final_price:.2f}"

# 1. Creating an empty object
item = Product()

# 2. Manually assigning the attributes directly to the object
item.name = "Wireless Headphones"
item.price = 89.99
item.discount = 15.00

# 3. Using the method to run calculations on those attributes
print(item.get_discount_price())  # Output: The final price for Wireless Headphones is $74.99