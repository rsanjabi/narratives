''' Unit test for Page objects'''

import unittest

from scrape.meta_temp import Meta


class TestMeta(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.page = Meta("Test Fandom", True)

    def tearDown(self):
        pass

    def test_init_(self):
        pass

    def test_scrape(self):
        pass

    def test_init_log(self):
        pass

    def test_start_from_top(self):
        pass


if __name__ == "__main__":
    unittest.main()
