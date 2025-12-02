import httpx
import sys

def test_uuid_validation():
    """Functional test for UUID validation endpoint"""
    
    url = "http://localhost:5000/uuid"
    valid_uuid = "4e136eb7-cfa9-11f0-8eb1-000d3a4fd085"
    
    print("Testing UUID validation endpoint...")
    
    # Test 1: Valid UUID
    print("\n1. Testing valid UUID...")
    response = httpx.post(url, data={'uuid': valid_uuid})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "Token validated successfully" in response.text
    print("   ✓ Valid UUID accepted")
    
    # Test 2: Invalid UUID
    print("\n2. Testing invalid UUID...")
    response = httpx.post(url, data={'uuid': 'invalid-token-123'})
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    assert "Token validation failed" in response.text
    print("   ✓ Invalid UUID rejected")
    
    # Test 3: Another invalid UUID
    print("\n3. Testing another invalid UUID...")
    response = httpx.post(url, data={'uuid': '00000000-0000-0000-0000-000000000000'})
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print("   ✓ Wrong UUID rejected")
    
    print("\n✅ All functional tests passed!")

if __name__ == '__main__':
    try:
        test_uuid_validation()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
