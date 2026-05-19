# List Comprehension: Temperature Converter
celsius_temps = [0, 10, 20, 37, 40] # Source data: Temperatures in Celsius
fahrenheit_temps = [(c * 9/5) + 32 for c in celsius_temps] # List Comprehension converting C to F
print("Celsius:", celsius_temps)
print("Fahrenheit:", fahrenheit_temps)

#List Comprehension with Filtering: E-commerce Cart
cart_prices = [12.99, 99.50, 45.00, 150.00, 9.99, 75.25]
premium_items = [price for price in cart_prices if price > 50] # Filter: Only keep prices greater than 50
print("All prices:", cart_prices)
print("Premium prices:", premium_items)

# String Manipulation (List Comprehension)
sentence = "Python is beautiful"
vowels = "aeiouAEIOU"
disemvoweled = [char for char in sentence if char not in vowels] # Keep the character only if it is NOT a vowel
clean_text = "".join(disemvoweled) # Join the list back into a single string
print("Original:", sentence)
print("No Vowels:", clean_text)
