import unittest
from unittest.mock import patch
import requests


def fetchDataFromAPI(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("Invalid data format: Expecting a non-empty list.")
        return data
    except requests.exceptions.RequestException as e:
        raise Exception(f"API Error: {e}") from e
    except ValueError as e:
        raise Exception(f"Data Validation Error: {e}") from e


class TestFetchDataFromAPI(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_data_success(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [1, 2, 3]
        mock_get.return_value = mock_response
        data = fetchDataFromAPI("http://example.com/api/data")
        self.assertEqual(data, [1, 2, 3])

    @patch('requests.get')
    def test_fetch_data_api_error(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_get.return_value = mock_response
        with self.assertRaises(Exception) as context:
            fetchDataFromAPI("http://example.com/api/data")
        self.assertEqual(str(context.exception), "API Error: 404 Client Error")

    @patch('requests.get')
    def test_fetch_data_invalid_data_format(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = "Invalid Data"
        mock_get.return_value = mock_response
        with self.assertRaises(Exception) as context:
            fetchDataFromAPI("http://example.com/api/data")
        self.assertEqual(str(context.exception),
                         "Data Validation Error: Invalid data format: Expecting a non-empty list.")

    @patch('requests.get')
    def test_fetch_data_empty_response(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        with self.assertRaises(Exception) as context:
            fetchDataFromAPI("http://example.com/api/data")
        self.assertEqual(str(context.exception),
                         "Data Validation Error: Invalid data format: Expecting a non-empty list.")

    @patch('requests.get')
    def test_fetch_data_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout
        with self.assertRaises(Exception) as context:
            fetchDataFromAPI("http://example.com/api/data")
        self.assertEqual(str(context.exception), "API Error: ")


if __name__ == '__main__':
    unittest.main()
