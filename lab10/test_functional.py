import httpx
import sys

def test_jwt_service():
    url = "http://localhost:5000/"
    
    print("=== JWT Service Functional Tests ===\n")
    print("1. Testing root endpoint...")
    try:
        response = httpx.get(url)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert "JWT Token Service" in response.text
        print("Root endpoint works")
    except Exception as e:
        print(f"Failed: {e}")
        return False
    
    print("\n2. Getting JWT token...")
    try:
        response = httpx.get(url + "token")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        token_data = response.json()
        assert "token" in token_data, "Token not in response"
        token = token_data["token"]
        print(f"Token received: {token[:50]}...")
    except Exception as e:
        print(f"Failed: {e}")
        return False
    
    print("\n3. Verifying valid token...")
    try:
        response = httpx.post(url + "verify", data={"token": token})
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        verify_data = response.json()
        assert verify_data["status"] == "valid", "Token not valid"
        assert "payload" in verify_data, "No payload in response"
        print("Valid token verified successfully")
    except Exception as e:
        print(f"Failed: {e}")
        return False
    
    print("\n4. Testing invalid token rejection...")
    try:
        response = httpx.post(url + "verify", data={"token": "invalid-token-123"})
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        error_data = response.json()
        assert "error" in error_data, "No error message"
        print("Invalid token correctly rejected")
    except Exception as e:
        print(f"Failed: {e}")
        return False
    
    print("\n5. Accessing protected resource with valid token...")
    try:
        response = httpx.post(url + "protected", data={"token": token})
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        protected_data = response.json()
        assert "message" in protected_data, "No message in response"
        assert protected_data["user_id"] == 1, "Wrong user_id"
        print("Protected resource accessed successfully")
    except Exception as e:
        print(f"Failed: {e}")
        return False
    
    print("\n6. Testing protected resource with invalid token...")
    try:
        response = httpx.post(url + "protected", data={"token": "bad-token"})
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        error_data = response.json()
        assert "error" in error_data, "No error message"
        print("Invalid token correctly denied access")
    except Exception as e:
        print(f"Failed: {e}")
        return False
    
    print("\n7. Testing missing token handling...")
    try:
        response = httpx.post(url + "protected", data={})
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        error_data = response.json()
        assert "error" in error_data, "No error message"
        print("Missing token correctly rejected")
    except Exception as e:
        print(f"Failed: {e}")
        return False
    
    print("\n7. Testing missing token handling...")
    return True

if __name__ == '__main__':
    try:
        success = test_jwt_service()
        sys.exit(0 if success else 1)
    except httpx.ConnectError:
        print("\n Error: Cannot connect to server at http://localhost:5000")
        print("Make sure the server is running: bin/python my-server.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n Test failed with error: {e}")
        sys.exit(1)
