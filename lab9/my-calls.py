import httpx
import uuid

#url = "https://cautious-doodle-pjpjx694jxvcr944-5000.app.github.dev/"

url = "http://localhost:5000/"

response = httpx.get(url)
print(response.status_code)
print(response)



response = httpx.get(url)
print(response.status_code)
print(response.text)

mydata = {
    "uuid": uuid.uuid1(),
    "text": "Hello Jhon!",
    "param2": "Making a POST request",
    "body": "my own value"
}

# A POST request to the API
response = httpx.post(url + "echo", data=mydata)

# Print the response
print(response.status_code)
print(response.text)

# Test the UUID token validation
print("\n--- Testing UUID Token Validation ---")
token_data = {"uuid": str(mydata["uuid"])}
response = httpx.post(url + "uuid", data=token_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}") 