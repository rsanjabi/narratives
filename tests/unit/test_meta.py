# from urllib.request import urlopen
# from bs4 import BeautifulSoup
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
        # url = (f'https://archiveofourown.org/tags/'
        #       f'Star%20Wars%20-%20All%20Media%20Types/works')
        # print(url)
        # TestMeta.bs = BeautifulSoup(urlopen(url), 'html.parser')
        pass

    def tearDown(self):
        pass

    def test_titleText(self):
        # pageTitle = TestMeta.bs.find('h1').get_text()
        # self.assertEqual('\nArchive of Our Own beta\n', pageTitle)
        pass

    def test_contentExists(self):
        content = TestMeta.bs.find('div')
        self.assertIsNotNone(content)
        pass

    def test_get_tag_info(self):
        pass


if __name__ == "__main__":
    unittest.main()
