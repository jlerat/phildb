import os
import numpy as np
import pandas as pd
import unittest
from datetime import datetime

from phildb import reader

class ReaderTest(unittest.TestCase):
    def setUp(self):
        self.tsdb_file = os.path.join(os.path.dirname(__file__), 'test_data', 'sample.tsdb')
        self.tsdb_file_with_missing = os.path.join(os.path.dirname(__file__), 'test_data', 'sample_missing.tsdb')
        self.empty_tsdb_file = os.path.join(os.path.dirname(__file__), 'test_data', 'empty.tsdb')

    def test_read(self):
        data = reader.read(self.tsdb_file)

        self.assertEqual(datetime(2014,1,1), data.index[0].to_pydatetime())
        self.assertEqual(datetime(2014,1,2), data.index[1].to_pydatetime())
        self.assertEqual(datetime(2014,1,3), data.index[2].to_pydatetime())

        self.assertEqual(1.0, data.values[0])
        self.assertEqual(2.0, data.values[1])
        self.assertEqual(3.0, data.values[2])

    def test_read_missing(self):
        data = reader.read(self.tsdb_file_with_missing)

        self.assertEqual(datetime(2014,1,1), data.index[0].to_pydatetime())
        self.assertEqual(datetime(2014,1,2), data.index[1].to_pydatetime())
        self.assertEqual(datetime(2014,1,3), data.index[2].to_pydatetime())
        self.assertEqual(datetime(2014,1,4), data.index[3].to_pydatetime())
        self.assertEqual(datetime(2014,1,5), data.index[4].to_pydatetime())
        self.assertEqual(datetime(2014,1,6), data.index[5].to_pydatetime())

        self.assertEqual(1.0, data.values[0])
        self.assertEqual(2.0, data.values[1])
        self.assertEqual(3.0, data.values[2])
        self.assertTrue(np.isnan(data.values[3]))
        self.assertEqual(5.0, data.values[4])
        self.assertEqual(6.0, data.values[5])

    def test_read_empty(self):
        data = reader.read(self.empty_tsdb_file)
        self.assertEqual(0, len(data))

    def test_read(self):
        data = reader.read('/tmp/not_an_actual_existing_file')

        self.assertEqual(0, len(data))
