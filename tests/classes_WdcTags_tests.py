import unittest

from wdc.classes import WdcTags


class WdcTagsFixture(unittest.TestCase):

    def test_valid(self):
        tags = WdcTags(['tag1', 'a', 'b'])

        test_result = str(tags)

        self.assertEqual('A,B,TAG1', test_result)

    def test_empty_list(self):
        tags = WdcTags([])

        test_result = str(tags)

        self.assertEqual('', test_result)
