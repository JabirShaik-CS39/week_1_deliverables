student = {
    "name": "Jabir",
    "age": 21,
    "course": "Python"
}
print(student)
print(student["name"])
print(student["age"])

print(student.keys()) # prints only keys
print(student.values()) # prints only values
print(student.items())# prints both keys and values in a tuple form

# Add item
student["marks"] = 95

# Update item
student["age"] = 22
student["course"] = "Data Structures"
print(student)

# Print all data in a row form
for key, value in student.items():
    print(key, ":", value)


# Nested Dictionary
students = {
    "student1": {
        "name": "Ali",
        "marks": 85
    },
    "student2": {
        "name": "Sara",
        "marks": 92
    }
}

print(students["student1"]["name"])
print(students["student2"]["marks"])
print(students)