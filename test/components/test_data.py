from unittest.mock import MagicMock, patch
from unittest import TestCase

from src.components.data import _download_table


class TestData(TestCase):
    @patch("requests.get")
    @patch("json.loads")
    def test__download_table_404_error(self, json_loads: MagicMock, request_get: MagicMock):
        class ReturnedValue:
            def __init__(self):
                self.reason=None
                self.status_code=404

        request_get.return_value = ReturnedValue()
        with self.assertRaises(Exception):
            _download_table("some_page", 55)

        request_get.assert_called_with(f'https://en.wikipedia.org/w/api.php?format=json&page=some_page&action=parse&prop=text&section=55')
        json_loads.assert_not_called()

