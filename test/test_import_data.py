import unittest
from unittest.mock import patch, Mock
import src.import_data

class TestImportData(unittest.TestCase):
    @patch('src.import_data.requests.get')
    @patch('src.import_data.os.makedirs')
    def test_get_drivers_standings(self, mock_makedirs, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'MRData': {
                'StandingsTable': {
                    'StandingsLists': [{
                        'DriverStandings': [{
                            'Driver': {
                                'givenName': 'Test',
                                'familyName': 'Driver'
                            },
                            'points': '100'
                        }]
                    }]
                }
            }
        }
        mock_get.return_value = mock_response

        # Call the function
        src.import_data.get_drivers_standings()

        # Check that requests.get was called with the correct URL
        mock_get.assert_called_once_with('http://ergast.com/api/f1/current/driverStandings.json')

        # Check that os.makedirs was called with the correct directory name
        self.assertTrue(mock_makedirs.called)

if __name__ == '__main__':
    unittest.main()