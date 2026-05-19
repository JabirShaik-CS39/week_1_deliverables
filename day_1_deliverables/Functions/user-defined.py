# Standard Greeting Generator
def Greeting(name, time_of_day):
    return f"Good {time_of_day}, {name}!"
msg = Greeting("Sarah", "morning")
print(msg)  

# Discount Calculator
def calculate_discount(price, discount_percentage):
    discount_amount = price * (discount_percentage / 100)
    return price - discount_amount
final_price = calculate_discount(150, 20)  
print(f"${final_price}")  