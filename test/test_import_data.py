import unittest
from src.import_data import mean

class TestImportData(unittest.TestCase):
    def test_mean(self):
        self.assertEqual(mean([1, 2, 3, 4, 5]), 3)
        self.assertEqual(mean([0, 0, 0, 0, 0]), 0)
        self.assertEqual(mean([-1, 0, 1]), 0)
        self.assertAlmostEqual(mean([1, 2.5, 3.5]), 2.3333333333333335)

if __name__ == '__main__':
    unittest.main()