# Tuples 
nums = (10, 20, 30, 40, 50, 30, 40, 50)
print(nums)

#adding two tuples
t1 = (1, 2)
t2 = (3, 4)

print(t1 + t2)

# count method
print(nums.count(30))


# index method
print(nums.index(40))

# slicing
print(nums[2:5])

# finding a item in a tuple
if 15 in nums:
    print("Found")
else:
    print("Not Found")

# converting a string to a tuple
text = "jabir"
result = tuple(text)

print(result)