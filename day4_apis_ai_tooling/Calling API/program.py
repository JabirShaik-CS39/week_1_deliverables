import requests

# Set up the dummy API URL (just like typing it into the Postman URL bar)
BASE_URL = "https://jsonplaceholder.typicode.com/posts"

print("--- STEP 1: EXECUTING GET REQUEST (Fetching Data) ---")

# 1. Fire a GET request to look at post ID #1
# Equivalent to putting 'https://jsonplaceholder.typicode.com/posts/1' into Postman
get_response = requests.get(f"{BASE_URL}/1")

# Look at the status code (Like checking 'Status: 200 OK' in Postman)
print(f"GET Status Code: {get_response.status_code}")

# Extract and print the JSON response data
if get_response.status_code == 200:
    data = get_response.json()
    print("Data received from server:")
    print(f"  - User ID: {data['userId']}")
    print(f"  - Post ID: {data['id']}")
    print(f"  - Title:   {data['title']}")
else:
    print("Failed to fetch data.")


print("\n" + "="*50 + "\n")


print("--- STEP 2: EXECUTING POST REQUEST (Sending Data) ---")

# 2. Define the new data payload (Like writing in Postman's 'Body -> raw -> JSON' tab)
new_post_payload = {
    "title": "Running APIs from VS Code",
    "body": "Now that requests is installed, I am hitting endpoints directly through Python!",
    "userId": 7
}

# Define headers to tell the server we are sending JSON data
custom_headers = {
    "Content-Type": "application/json"
}

# Fire the POST request, passing the json data dictionary directly
post_response = requests.post(BASE_URL, json=new_post_payload, headers=custom_headers)

# Look at the status code (Like checking for 'Status: 201 Created' in Postman)
print(f"POST Status Code: {post_response.status_code}")

# See what the server generated and sent back to you
if post_response.status_code == 201:
    created_data = post_response.json()
    print("Server response confirming creation:")
    print(created_data)
else:
    print("Failed to create new record.")