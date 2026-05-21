import requests
import json

# Define the endpoint URL
url = "https://jsonplaceholder.typicode.com/posts"

# Define the payload data
payload = {
    "title": "My First Postman Request",
    "body": "Postman makes dealing with APIs incredibly straightforward.",
    "userId": 1
}

# Define the required headers
headers = {
    "Content-Type": "application/json"
}

# Execute the POST request
response = requests.post(url, data=json.dumps(payload), headers=headers)

# Print out the server response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())