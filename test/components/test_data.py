from unittest.mock import MagicMock, patch
from unittest import TestCase
from requests.models import Response
from requests.exceptions import HTTPError
from pandas import read_csv

from src.components.data import _download_table, InvalidContentFromWikipedia


with open('html_content_sample.txt') as f:
    GOOD_HTML_CONTENT = f.read()

GOOD_DATA_FRAME = read_csv('data_frame_content_sample.csv')

def _generate_response_json (html_content: str) -> str:
    return f'{{ "parse": {{ "title": "List of most-visited museums", "pageid": 54754776, "text": {{ "*": "{html_content}" }} }} }}'

class TestData(TestCase):
    @patch("requests.get")
    @patch("json.loads")
    def test__download_table_404_error(self, json_loads: MagicMock, request_get: MagicMock):
        class ReturnedValue(Response):
            def __init__(self):
                self.reason=None
                self.status_code=404
                self.url = "https://some.url"

        test_page='some_page'
        test_section=55
        request_get.return_value = ReturnedValue()
        with self.assertRaises(HTTPError):
            _download_table(test_page, test_section)

        request_get.assert_called_with(f'https://en.wikipedia.org/w/api.php?format=json&page={test_page}&action=parse&prop=text&section={test_section}')
        json_loads.assert_not_called()

    @patch("requests.get")
    def test__download_table_empty_html(self, request_get: MagicMock):
        class ReturnedValue(Response):
            def __init__(self):
                super()
                self.reason = None
                self.status_code = 200
                self.url = "https://some.url"

            @property
            def text(self) -> str:
                return _generate_response_json("")

        test_page = 'some_page'
        test_section = 55
        request_get.return_value = ReturnedValue()
        with self.assertRaises(InvalidContentFromWikipedia):
            _download_table(test_page, test_section)

        request_get.assert_called_with(
            f'https://en.wikipedia.org/w/api.php?format=json&page={test_page}&action=parse&prop=text&section={test_section}')

    @patch("requests.get")
    def test__download_table_success(self, request_get: MagicMock):
        class ReturnedValue(Response):
            def __init__(self):
                super()
                self.reason=None
                self.status_code=200
                self.url = "https://some.url"

            @property
            def text(self) -> str:
                return _generate_response_json(GOOD_HTML_CONTENT)

        test_page='some_page'
        test_section=55
        request_get.return_value = ReturnedValue()
        test_df = _download_table(test_page, test_section)
        self.assertTrue(test_df.equals(GOOD_DATA_FRAME))
        request_get.assert_called_with(f'https://en.wikipedia.org/w/api.php?format=json&page={test_page}&action=parse&prop=text&section={test_section}')

