# Dealing with files
import json
my_data = {"project": "Knowledge Factory", "Batch": 6}
with open("data.json", "w") as file_object:  # Open a new file called 'data.json' in write mode ('w')
    json.dump(my_data, file_object, indent=4)  # This creates a file on your computer with formatted JSON text
with open("data.json", "r") as file_object:  # Open the same file in read mode ('r')
    loaded_data = json.load(file_object)
print(loaded_data["project"]) 