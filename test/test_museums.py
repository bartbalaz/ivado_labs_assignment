from unittest.mock import MagicMock, patch
from unittest import TestCase
from src.museums import load_master_data

class TestData(TestCase):
    @patch('pandas.read_csv')
    @patch('os.path.exists')
    def test_load_master_data_file_does_not_exist(self, os_path_exists: MagicMock, pandas_read_cvs: MagicMock):
        test_file_name = 'some_file'
        os_path_exists.return_value = False
        with self.assertRaises(Exception):
            load_master_data('some_file')
        os_path_exists.assert_called_with(test_file_name)
        pandas_read_cvs.assert_not_called()
