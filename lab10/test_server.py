import unittest
import sys
import importlib.util
import jwt
import datetime

spec = importlib.util.spec_from_file_location("my_server", "/workspaces/j2025-12-2-CSE2102-Final/lab10/my-server.py")
my_server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(my_server)
app = my_server.app
SECRET_KEY = my_server.SECRET_KEY

class TestJWTEndpoints(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct message"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'JWT Token Service', response.data)
    
    def test_get_token(self):
        """Test token generation endpoint"""
        response = self.app.get('/token')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('token', data)
        self.assertIsInstance(data['token'], str)
        decoded = jwt.decode(data['token'], SECRET_KEY, algorithms=["HS256"])
        self.assertIn('user_id', decoded)
        self.assertIn('jti', decoded)
    
    def test_verify_valid_token(self):
        """Test verifying a valid token"""
        token_response = self.app.get('/token')
        token = token_response.get_json()['token']
        
        response = self.app.post('/verify', data={'token': token})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'valid')
        self.assertIn('payload', data)
    
    def test_verify_invalid_token(self):
        """Test verifying an invalid token"""
        response = self.app.post('/verify', data={'token': 'invalid-token'})
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_verify_missing_token(self):
        """Test verify endpoint with missing token"""
        response = self.app.post('/verify', data={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Missing token')
    
    def test_protected_with_valid_token(self):
        """Test accessing protected resource with valid token"""
        token_response = self.app.get('/token')
        token = token_response.get_json()['token']
        
        response = self.app.post('/protected', data={'token': token})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['user_id'], 1)
    
    def test_protected_with_invalid_token(self):
        """Test accessing protected resource with invalid token"""
        response = self.app.post('/protected', data={'token': 'bad-token'})
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_protected_without_token(self):
        """Test accessing protected resource without token"""
        response = self.app.post('/protected', data={})
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Missing token')
    
    def test_expired_token(self):
        """Test with an expired token"""
        payload = {
            "user_id": 1,
            "exp": datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)
        }
        expired_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        response = self.app.post('/protected', data={'token': expired_token})
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('expired', data['error'].lower())

if __name__ == '__main__':
    unittest.main()
