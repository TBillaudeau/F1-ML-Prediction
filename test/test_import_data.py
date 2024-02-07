import unittest
from unittest.mock import patch, mock_open, MagicMock
import src.import_data as import_data


class TestImportData(unittest.TestCase):

    @patch('src.import_data.os.path.join')
    @patch('src.import_data.glob.glob')
    @patch('src.import_data.os.path.getmtime')
    def test_get_most_recent_dir(self, mock_getmtime, mock_glob, mock_join):
        # Setup the mocks
        mock_join.return_value = "data/api_ergast/*"
        mock_glob.return_value = ['data/api_ergast/dir1', 'data/api_ergast/dir2']
        mock_getmtime.side_effect = lambda x: {'data/api_ergast/dir1': 1, 'data/api_ergast/dir2': 2}[x]

        # Call the function
        most_recent_dir = import_data.get_most_recent_dir()

        # Assert the expected output
        self.assertEqual(most_recent_dir, 'data/api_ergast/dir2')

    @patch('src.import_data.pd.read_csv')
    @patch('src.import_data.os.path.join')
    def test_import_files(self, mock_join, mock_read_csv):
        # Setup the mocks
        mock_join.side_effect = lambda *args: "/".join(args)
        mock_read_csv.return_value = MagicMock()

        # Call the function
        last_results, last_races = import_data.import_files('data/api_ergast/dir2')

        # Assert that read_csv was called correctly
        mock_read_csv.assert_any_call('data/api_ergast/dir2/results.csv')
        mock_read_csv.assert_any_call('data/api_ergast/dir2/races.csv')

    @patch('src.import_data.requests.get')
    def test_get_api_data(self, mock_get):
        # Setup the mocks
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'MRData': {
                'RaceTable': {
                    'Races': [{'raceName': 'Some Grand Prix'}]
                }
            }
        }
        mock_get.return_value = mock_response

        # Call the function
        results, raceName = import_data.get_api_data()

        # Assert the expected output
        self.assertEqual(raceName, 'Some Grand Prix')
        self.assertEqual(len(results), 1)

if __name__ == '__main__':
    unittest.main()
