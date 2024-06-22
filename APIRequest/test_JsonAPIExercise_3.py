import unittest
from unittest.mock import patch
from JSON_API_Exercise_3 import JsonAPIExercise3

class TestJsonAPIExcercise3(unittest.TestCase):

    def test_json_api_statuscode_200_ok(self):
        sample_authorID = 4

        with patch("JSON_API_Exercise_3.requests.get") as mock_get:
            mock_get.return_value.status_code = 200

            obj = JsonAPIExercise3()
            obj.set_author_id(sample_authorID)
            response = obj.getAuthors()
            
        self.assertEqual(response.status_code, 200)
        
    def test_json_api_statuscode_400_bad_request(self):
        sample_authorID = 600

        with patch("JSON_API_Exercise_3.requests.get") as mock_get:
            mock_get.return_value.status_code = 400

            obj = JsonAPIExercise3()
            obj.set_author_id(sample_authorID)
            response = obj.getAuthors()

        self.assertEqual(response.status_code, 400)


    def test_json_api_raise_exception(self):
        sample_authorID = 1000

        with patch("JSON_API_Exercise_3.requests.get") as mock_get:
            mock_get.return_value.status_code = 400

            obj = JsonAPIExercise3()
            obj.set_author_id(sample_authorID)

        self.assertRaises(ValueError)
        

if __name__ == "__main__":
    unittest.main()