import httpx

url = "http://localhost:5000/"

print("=== JWT Token Service Test ===\n")

print("1. Testing root endpoint...")
response = httpx.get(url)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.text}")

print("\n2. Getting a JWT token...")
response = httpx.get(url + "token")
print(f"   Status: {response.status_code}")
token_data = response.json()
print(f"   Response: {token_data}")
token = token_data['token']
print(f"   Token: {token[:50]}...")

print("\n3. Verifying the token...")
response = httpx.post(url + "verify", data={'token': token})
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")

print("\n4. Accessing protected resource with valid token...")
response = httpx.post(url + "protected", data={'token': token})
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")

print("\n5. Testing with invalid token...")
response = httpx.post(url + "protected", data={'token': 'invalid-token-123'})
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")

print("\n=== All tests completed ===")
