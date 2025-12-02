import unittest
import sys
import importlib.util

# Load my-server.py as a module
spec = importlib.util.spec_from_file_location("my_server", "/workspaces/j2025-12-2-CSE2102-Final/my-server.py")
my_server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(my_server)
app = my_server.app

class TestUUIDEndpoint(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.valid_uuid = "4e136eb7-cfa9-11f0-8eb1-000d3a4fd085"
    
    def test_valid_uuid(self):
        """Test with correct UUID token"""
        response = self.app.post('/uuid', data={'uuid': self.valid_uuid})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Token validated successfully', response.data)
    
    def test_invalid_uuid(self):
        """Test with incorrect UUID token"""
        response = self.app.post('/uuid', data={'uuid': 'wrong-token'})
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Token validation failed', response.data)
    
    def test_missing_uuid(self):
        """Test with missing UUID parameter"""
        response = self.app.post('/uuid', data={})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
