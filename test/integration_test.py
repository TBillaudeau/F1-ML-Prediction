import unittest
import src.import_data as import_data
import pandas as pd
import os

class TestImportDataIntegration(unittest.TestCase):

    def test_integration(self):
        # Call get_most_recent_dir and check the result
        most_recent_dir = import_data.get_most_recent_dir()
        self.assertTrue(os.path.isdir(most_recent_dir))

        # Call get_api_data and check the results
        results, raceName = import_data.get_api_data()
        self.assertIsNotNone(results)
        self.assertIsInstance(raceName, str)

        # Call import_files and check the results
        last_results, last_races, last_drivers, last_constructors = import_data.import_files(most_recent_dir)
        self.assertIsInstance(last_results, pd.DataFrame)
        self.assertIsInstance(last_races, pd.DataFrame)
        self.assertIsInstance(last_drivers, pd.DataFrame)
        self.assertIsInstance(last_constructors, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()