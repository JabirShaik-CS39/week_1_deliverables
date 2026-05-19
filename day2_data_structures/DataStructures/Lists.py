# Lists are ordered, mutable, and allow duplicate elements.
Vegitables = ["Tomato", "Cucumber", "Carrot", "Lettuce", "Spinach"]
Vegitables.append("Broccoli")   # Adds "Broccoli" to the end of the list
Vegitables.remove("Carrot") # Removes the first occurrence of "Carrot" from the list
Vegitables.insert(2, "Onion")  # Inserts "Onion" at index 2
Vegitables.pop(-2)# Removes and returns the last item ("Broccoli")
print(Vegitables)
Vegitables=list(sorted(Vegitables))
print(Vegitables)
print(Vegitables[2])
print(Vegitables[1:4])
Vegitables.insert(-1, "Mushroom")
print(Vegitables)
Vegitables.reverse()
print(Vegitables)
Vegitables.sort()
print(Vegitables)
len(Vegitables)
print(len(Vegitables))

