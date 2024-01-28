import unittest
import os
import pandas as pd
from src.import_data import get_drivers_standings

class TestImportData(unittest.TestCase):
    def setUp(self):
        self.year = 'current'
        self.filepath = 'data/api_ergast/driver_standings.csv'

    def test_get_drivers_standings(self):
        # Run the function
        get_drivers_standings(self.year)

        # Check if the CSV file was created
        self.assertTrue(os.path.exists(self.filepath))

        # Check if the CSV file is not empty
        df = pd.read_csv(self.filepath)
        self.assertTrue(not df.empty)

if __name__ == '__main__':
    unittest.main()