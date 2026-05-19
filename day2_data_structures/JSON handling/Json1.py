# Moving from Python ----> JSON
import json
employee = {    # 1. This is a real Python Dictionary (the built furniture)
    "name": "Jabir",
    "age": 24,
    "remote_worker": False
}
json_string = json.dumps(employee)# 2. Convert it to a flat string (flat-packing it for shipping)
print(type(json_string))  
print(json_string)        

