import unittest
from maccli.helper.unsortable import ordered_load, yaml

from mock_data import *


class UnsortableTestCase(unittest.TestCase):

    def test_int_as_string(self):
        mock_yaml = "test: 2"
        expected = OrderedDict([(u'test', u'2')])
        raw = ordered_load(mock_yaml, yaml.BaseLoader)
        self.assertEqual(raw, expected)

