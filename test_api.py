import unittest
import json
from MainInterface import app, db  # Ensure you import your Flask app and db instance

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        # Configure the app for testing
        app.config['TESTING'] = True
        # Use an in-memory SQLite database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up after each test
        with app.app_context():
            db.drop_all()

    def test_add_and_get_phone(self):
        # Define a sample payload for a MobilePhone record
        payload = {
            "serial_number": "ABC12345678",
            "imei": "123456789012345",
            "model": "X100",
            "brand": "Nokia",
            "network_technologies": ["GSM", "LTE"],
            "number_of_cameras": 2,
            "number_of_cores": 4,
            "weight": 150,
            "battery_capacity": 3000,
            "cost": 299.99
        }
        # Send a POST request to add a phone
        response = self.app.post('/add_phone', data=json.dumps(payload), content_type='application/json')
        print("\ntest_add_and_get_phone: ", response.data)
        self.assertEqual(response.status_code, 201)

        # Send a GET request to retrieve all phone records
        response = self.app.get('/phones')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Confirm that the newly added phone is in the returned data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['serial_number'], payload['serial_number'])
    
    def test_invalid_phone(self):
        # Define an invalid payload with missing required fields
        payload = {
            "imei": "123456789012345",
            "model": "X100",
            "brand": "Nokia"
            # Missing other required fields like serial_number, network_technologies, etc.
        }
        # Send a POST request with the invalid payload
        response = self.app.post('/add_phone', data=json.dumps(payload), content_type='application/json')
        print("\ntest_invalid_phone", response.data)
        # Expect a 400 Bad Request response
        self.assertEqual(response.status_code, 400)


    def test_update_phone(self):
        # Add a phone first
        payload = {
            "serial_number": "DEF98765432",
            "imei": "987654321098765",
            "model": "Y200",
            "brand": "Samsung",
            "network_technologies": ["GSM", "5G"],
            "number_of_cameras": 3,
            "number_of_cores": 8,
            "weight": 180,
            "battery_capacity": 4000,
            "cost": 499.99
        }
        self.app.post(f'/add_phone', data=json.dumps(payload), content_type='application/json')

        # Define an update payload
        update_payload = {
            "cost": 450.00
        }
        # Send a PUT request to update the phone
        # Note: The serial number is not allowed to be updated, so we don't include it in the update payload.
        # The update payload should only include fields that are allowed to be updated.
        response = self.app.put(f"/update_phone/{payload['serial_number']}", data=json.dumps(update_payload), content_type='application/json')
        print('\nupdate: ', response.data)
        self.assertEqual(response.status_code, 200)

        # Verify the update
        response = self.app.get('/phones')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['cost'], update_payload['cost'])

    def test_delete_phone(self):
        # Add a phone first
        payload = {
            "serial_number": "GHI12345678",
            "imei": "123450987654321",
            "model": "Z300",
            "brand": "Apple",
            "network_technologies": ["LTE", "5G"],
            "number_of_cameras": 2,
            "number_of_cores": 6,
            "weight": 170,
            "battery_capacity": 3500,
            "cost": 999.99
        }
        self.app.post('/add_phone', data=json.dumps(payload), content_type='application/json')

        # Send a DELETE request to remove the phone
        response = self.app.delete(f"/delete_phone/{payload['serial_number']}")
        print("\ntest_delete_phone", response.data)
        self.assertEqual(response.status_code, 200)

        # Verify the phone is deleted
        response = self.app.get('/phones')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

    # Test the creation of 2 phones with the same serial number
    def test_duplicate_serial_number(self):
        payload = {
            "serial_number": "JKL12345678",
            "imei": "123456789012345",
            "model": "X100",
            "brand": "Nokia",
            "network_technologies": ["GSM", "LTE"],
            "number_of_cameras": 2,
            "number_of_cores": 4,
            "weight": 150,
            "battery_capacity": 3000,
            "cost": 299.99
        }
        # Add the first phone
        response = self.app.post('/add_phone', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Attempt to add a second phone with the same serial number
        response = self.app.post('/add_phone', data=json.dumps(payload), content_type='application/json')
        print("\ntest_duplicate_serial_number", response.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("already exists", str(response.data))

        # Verify that only one phone exists in the database
        response = self.app.get('/phones')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['serial_number'], payload['serial_number'])

    # Test that the route /phones and /phone/ return the same data
    def test_get_phones_routes(self):
        # Add a phone first
        payload = {
            "serial_number": "MNO12345678",
            "imei": "123456789012345",
            "model": "X100",
            "brand": "Nokia",
            "network_technologies": ["GSM", "LTE"],
            "number_of_cameras": 2,
            "number_of_cores": 4,
            "weight": 150,
            "battery_capacity": 3000,
            "cost": 299.99
        }
        self.app.post('/add_phone', data=json.dumps(payload), content_type='application/json')

        # Test /phones route
        response = self.app.get('/phones')
        self.assertEqual(response.status_code, 200)
        data_phones = json.loads(response.data)

        # Test /phone/ route
        response = self.app.get('/phone/')
        self.assertEqual(response.status_code, 200)
        data_phone = json.loads(response.data)

        # Compare the two responses
        self.assertEqual(data_phones, data_phone)
        # Ensure the data matches the added phone
        self.assertEqual(len(data_phones), 1)
        self.assertEqual(data_phones[0]['serial_number'], payload['serial_number'])
        # Ensure the data matches the added phone
        self.assertEqual(len(data_phone), 1)
        self.assertEqual(data_phone[0]['serial_number'], payload['serial_number'])
        
    # Test that the route /phones/<string:field>/<string:value> returns the correct phones
    def test_get_phones_by_field(self):
        # Add multiple phones
        phones = [
            {
                "serial_number": "PQR12345678",
                "imei": "123456789012345",
                "model": "X100",
                "brand": "Nokia",
                "network_technologies": ["GSM", "LTE"],
                "number_of_cameras": 2,
                "number_of_cores": 4,
                "weight": 150,
                "battery_capacity": 3000,
                "cost": 299.99
            },
            {
                "serial_number": "STU98765432",
                "imei": "987654321098765",
                "model": "Y200",
                "brand": "Samsung",
                "network_technologies": ["5G", "LTE"],
                "number_of_cameras": 3,
                "number_of_cores": 8,
                "weight": 180,
                "battery_capacity": 4000,
                "cost": 499.99
            }
        ]
        for phone in phones:
            self.app.post('/add_phone', data=json.dumps(phone), content_type='application/json')

        # Test filtering by number_of_cameras
        response = self.app.get('/phones/number_of_cameras/2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['serial_number'], "PQR12345678")

        # Test filtering by brand
        response = self.app.get('/phones/brand/Samsung')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['serial_number'], "STU98765432")

        # Test filtering by network_technologies (partial match)
        response = self.app.get('/phones/network_technologies/LTE')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)  # Both phones have LTE in their network_technologies

        # Test invalid field
        response = self.app.get('/phones/invalid_field/value')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid field", str(response.data))

        # Test invalid value type
        response = self.app.get('/phones/number_of_cameras/invalid')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid type for field number_of_cameras", str(response.data))

if __name__ == '__main__':
    unittest.main()
