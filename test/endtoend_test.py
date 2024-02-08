import unittest
import src.import_data as import_data
import src.train_and_save_model as ts_model
import os
import pandas as pd

class TestEndToEnd(unittest.TestCase):

    def test_end_to_end(self):
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

        # Call load_datasets and check the results
        races_df, results_df = ts_model.load_datasets(most_recent_dir)
        self.assertIsInstance(races_df, pd.DataFrame)
        self.assertIsInstance(results_df, pd.DataFrame)

        # Call preprocess_and_select_features and check the results
        X, y = ts_model.preprocess_and_select_features(races_df, results_df)
        self.assertIsInstance(X, pd.DataFrame)
        self.assertIsInstance(y, pd.Series)

        # Call split_data and check the results
        X_train, X_test, y_train, y_test = ts_model.split_data(X, y)
        self.assertIsInstance(X_train, pd.DataFrame)
        self.assertIsInstance(X_test, pd.DataFrame)
        self.assertIsInstance(y_train, pd.Series)
        self.assertIsInstance(y_test, pd.Series)

        # Call train_model and check the results
        model = ts_model.train_model(X_train, y_train)
        self.assertIsNotNone(model)

        # Call evaluate_model and check the results
        ts_model.evaluate_model(model, X_test, y_test)

if __name__ == '__main__':
    unittest.main()