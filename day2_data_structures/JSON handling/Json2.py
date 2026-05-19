#  Moving from JSON ----> Python
import json
incoming_reply = '{"status": "NotFound", "code": 403, "data": null}'   # 1. This is a raw string containing JSON data (the flat box)
python_dict = json.loads(incoming_reply)  # 2. Parse it so Python understands it natively (assembling the furniture)
print(type(python_dict))  
print(python_dict["status"])  