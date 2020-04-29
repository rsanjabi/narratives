from urllib.request import urlopen
from bs4 import BeautifulSoup
import unittest
# from unittest.mock import patch
# import scrape.meta as meta


class TestMeta(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        url = 'https://archiveofourown.org/tags/Star%20Wars%20-%20All%20Media%20Types/works'
        TestMeta.bs = BeautifulSoup(urlopen(url), 'html.parser')

    def tearDown(self):
        pass

    def test_titleText(self):
        pageTitle = TestMeta.bs.find('h1').get_text()
        self.assertEqual('\nArchive of Our Own beta\n', pageTitle)
   
    def test_contentExists(self):
        content = TestMeta.bs.find('div')
        self.assertIsNotNone(content)

    def test_get_tag_info(self):
        pass

if __name__ == "__main__":
    unittest.main()
