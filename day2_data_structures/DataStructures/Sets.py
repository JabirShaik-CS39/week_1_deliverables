# Sets are unordered collections of unique elements. They are mutable, meaning you can add or remove elements from a set after it has been created. Sets are defined using curly braces {} or the built-in set() function.
fruits = {"apple", "banana", "mango"}
print(fruits)
print(type(fruits))
# Sets do not allow duplicate elements. 
numbers = {1, 2, 3, 4, 5, 6,7, 8, 9, 10}
numbers.discard(5)
numbers.remove(3)
print(numbers)
# using loop in sets
for i in numbers:
    print(i)
print(3 in numbers)

# Set operations
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}
print(A.union(B))
print(A.intersection(B))
print(A.difference(B))
print(A.symmetric_difference(B))
print(A.issubset(B))
print(A.issuperset(B))
