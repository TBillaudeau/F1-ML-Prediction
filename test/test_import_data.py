import unittest
from unittest.mock import patch, MagicMock
import src.import_data as import_data
import pandas as pd
from pandas.testing import assert_frame_equal

class TestImportDataFunctions(unittest.TestCase):

    @patch('src.import_data.glob.glob')
    @patch('src.import_data.os.path.getmtime')
    @patch('src.import_data.os.path.join')
    def test_get_most_recent_dir(self, mock_join, mock_getmtime, mock_glob):
        mock_join.return_value = "data/api_ergast/*"
        mock_glob.return_value = ["data/api_ergast/dir1", "data/api_ergast/dir2"]
        mock_getmtime.side_effect = lambda x: {"data/api_ergast/dir1": 100, "data/api_ergast/dir2": 200}[x]
        
        most_recent_dir = import_data.get_most_recent_dir()
        self.assertEqual(most_recent_dir, "data/api_ergast/dir2")

    @patch('src.import_data.requests.get')
    def test_get_api_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "MRData": {
                "RaceTable": {
                    "Races": [{"raceName": "Example Race"}]

                }
            }
        }
        
        mock_get.return_value = mock_response
        results, raceName = import_data.get_api_data()
        
        self.assertIsNotNone(results)
        self.assertEqual(raceName, "Example Race")

        # Test for a failed API call
        mock_response.status_code = 404
        results, raceName = import_data.get_api_data()
        self.assertIsNone(results)
        self.assertIsNone(raceName)

    @patch('src.import_data.pd.read_csv')
    def test_import_files(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(data={'dummy': [1, 2]})
        most_recent_dir = "data/api_ergast/dir2"
        last_results, last_races, last_drivers, last_constructors = import_data.import_files(most_recent_dir)
        
        # Verify that all returned objects are DataFrames
        self.assertIsInstance(last_results, pd.DataFrame)
        self.assertIsInstance(last_races, pd.DataFrame)
        self.assertIsInstance(last_drivers, pd.DataFrame)
        self.assertIsInstance(last_constructors, pd.DataFrame)

        # Verify the mock was called with the correct path
        mock_read_csv.assert_any_call("data/api_ergast/dir2/results.csv")
        mock_read_csv.assert_any_call("data/api_ergast/dir2/races.csv")
        mock_read_csv.assert_any_call("data/api_ergast/dir2/drivers.csv")
        mock_read_csv.assert_any_call("data/api_ergast/dir2/constructors.csv")


if __name__ == '__main__':
    unittest.main()
