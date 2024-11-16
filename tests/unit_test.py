import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch
from io import StringIO
import sys
import os

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.creditRiskAnalysisImpl import (
    distOfNumericalColumns,
    distOfCategoricalColumns,
    correlationOfNumColumns,
    find_missing_values,
    aggregateFeatures,
    extractDateAndTime,
    encodingCategoricalVariables,
    calculateRFMSscores,
)



class TestFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up mock data for testing."""
        cls.mock_data = pd.DataFrame({
            'AccountId': [1, 2, 1, 3],
            'Amount': [100, 200, 150, 300],
            'TransactionId': [101, 102, 103, 104],
            'CurrencyCode': ['USD', 'EUR', 'USD', 'JPY'],
            'ProductCategory': ['Electronics', 'Clothing', 'Electronics', 'Food'],
            'TransactionStartTime': ['2024-10-01 12:30:00', '2024-10-02 14:00:00', '2024-10-03 10:00:00',
                                     '2024-10-04 09:15:00']
        })
        cls.mock_data['TransactionStartTime'] = pd.to_datetime(cls.mock_data['TransactionStartTime'])

    def test_find_missing_values(self):
        mock_data_with_missing = self.mock_data.copy()
        mock_data_with_missing.loc[0, 'Amount'] = np.nan
        summary = find_missing_values(mock_data_with_missing)
        self.assertEqual(summary.loc['Amount', 'Missing values'], 1)
        self.assertEqual(summary.loc['Amount', 'Percent of Total Values'], 25.0)

    def test_aggregateFeatures(self):
        aggregated = aggregateFeatures(self.mock_data)
        self.assertEqual(aggregated.loc[aggregated['AccountId'] == 1, 'TotalTransactionAmount'].values[0], 250)
        self.assertEqual(aggregated.loc[aggregated['AccountId'] == 3, 'TransactionCount'].values[0], 1)

    def test_extractDateAndTime(self):
        extracted = extractDateAndTime(self.mock_data.copy())
        self.assertIn('TransactionHour', extracted.columns)
        self.assertEqual(extracted.loc[0, 'TransactionHour'], 12)

    def test_encodingCategoricalVariables(self):
        encoded = encodingCategoricalVariables(self.mock_data.copy())
        self.assertNotIn('CurrencyCode', encoded.columns)
        self.assertTrue(any('CurrencyCode_' in col for col in encoded.columns))

    def test_calculateRFMSscores(self):
        mock_data_with_ids = self.mock_data.copy()
        mock_data_with_ids['CustomerId'] = [1, 2, 1, 3]
        rfms = calculateRFMSscores(mock_data_with_ids)
        self.assertIn('RFMS_Score', rfms.columns)
        self.assertEqual(rfms.loc[rfms.index[0], 'Frequency'], 2)

    @patch('matplotlib.pyplot.show')  # Patch plt.show to avoid rendering plots
    def test_distOfNumericalColumns(self, mock_show):
        distOfNumericalColumns(self.mock_data, ['Amount'])
        self.assertTrue(mock_show.called)

    @patch('matplotlib.pyplot.show')
    def test_distOfCategoricalColumns(self, mock_show):
        distOfCategoricalColumns(self.mock_data, ['CurrencyCode'])
        self.assertTrue(mock_show.called)

    @patch('matplotlib.pyplot.show')
    def test_correlationOfNumColumns(self, mock_show):
        correlationOfNumColumns(self.mock_data)
        self.assertTrue(mock_show.called)

if __name__ == '__main__':
    unittest.main()