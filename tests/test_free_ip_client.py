import unittest

from unittest.mock import patch, Mock

from requests.exceptions import RequestException

from free_ip_client import get_location, FREE_IP_API_URL


class TestFreeIpClient(unittest.TestCase):
    @patch("free_ip_client.requests.get")
    def test_get_location_returns_expected_data(self, mock_get: Mock):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "countryName": "USA",
            "cityName": "MIAMI",
            "regionName": "FLORIDA",
        }

        result = get_location("8.8.8.8")
        self.assertEqual(result["country"], "USA")
        self.assertEqual(result["region"], "FLORIDA")
        self.assertEqual(result["city"], "MIAMI")

        mock_get.assert_called_once_with(f"{FREE_IP_API_URL}/8.8.8.8")

    @patch("free_ip_client.requests.get")
    def test_get_location_returns_side_effect(self, mock_get: Mock):
        mock_get.side_effect = [
            RequestException("Service Unavailable"),
            Mock(
                status_code=200,
                json=lambda: {
                    "countryName": "USA",
                    "cityName": "MIAMI",
                    "regionName": "FLORIDA",
                },
            ),
        ]

        with self.assertRaises(RequestException):
            get_location("8.8.8.8")

        result = get_location("8.8.8.8")
        self.assertEqual(result["country"], "USA")
        self.assertEqual(result["region"], "FLORIDA")
        self.assertEqual(result["city"], "MIAMI")

    def test_get_location_on_invalid_ip_raises_exception(self):
        with self.assertRaises(ValueError):
            get_location("invalid_ip_address")
