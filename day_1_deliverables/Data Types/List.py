Vehicles = ["car", "van", "bus", "lorry", "truck","bike","ship","train","plane","helicopter","helicopter","boat"]
print(Vehicles)

# reverse the list
Vehicles.reverse()
print(Vehicles)

# remove a item from the list
Vehicles.remove("car")
print(Vehicles)

# add a item to the list
Vehicles.append("car")      
print(Vehicles)

# insert a item to the list
Vehicles.insert(1, "submarine")
print(Vehicles)

# find item in a list
if "car" in Vehicles:
    print("Present")
else:
    print("Not Present")

# find the index of an item in a list
index = Vehicles.index("car")   
print(index)

# Remove the last item from the list
Vehicles.pop()
print(Vehicles)

# Remove duplicate items from the list
Vehicles = list(set(Vehicles))
print(Vehicles)

# Sort the list
Vehicles.sort()
print(Vehicles)

# sort the list in descending order
Vehicles.sort(reverse=True)
print(Vehicles)

#common items in two lists
list1 = [1, 2, 3, 4, 5]
list2 = [3, 4, 5, 6, 7]

common = []

for i in list1:
    if i in list2:
        common.append(i)

print("Common elements:", common)

# count the number of even and odd numbers in a list
numbers = [1, 2, 3, 4, 5, 6]

even = 0
odd = 0

for i in numbers:
    if i % 2 == 0:
        even += 1
    else:
        odd += 1

print("Even:", even)
print("Odd:", odd)

# slicing a list
print(Vehicles[2:5])

List = [] 
for i in range(5):
    List.append(input("Enter a item: "))
print(List)