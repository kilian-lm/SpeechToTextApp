# Import necessary libraries for testing
import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        print(response.status_code)
        
        # self.assertIn(b'Hello, world!', response.data)

    # Add more test cases for other routes and functionality

if __name__ == '__main__':
    unittest.main()
