import unittest

from wdc.helper.io import array_to_tags_string


class ArrayToTagsString(unittest.TestCase):

    def test_valid(self):
        tags_list = ['tag1', 'a', 'b']

        test_result = array_to_tags_string(tags_list)

        self.assertEqual('a,b,tag1', test_result)

    def test_empty_list(self):
        tags_list = []

        test_result = array_to_tags_string(tags_list)

        self.assertEqual('', test_result)
