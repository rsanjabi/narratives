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
        pass

    def tearDown(self):
        pass

    def test_get_tag_info(self):
        pass

        '''
        result = meta.get_tag_info(1, 1)
        self.assertEqual(type(result), [])

        with self.assertRaises(ValueError):
            meta.get_tag_info()
        '''


'''
example:
    def monthly_schedule(self, month):
        response = requests.get(f'http://company.com/{self.last}/{month}')
        if response.ok:
            return response.text
        else:
            return 'Bad Response!'
example test:
    def test_monthly_schedule(self):
        # from employee module requests.get
        with patch('employee.requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = 'Success'

            schedule = self.emp1.monthly_schedule('May')
            mocked_get.assert_called_with('http://company.com/Schafer/May')
            self.assertEqual(schedule, 'Success')

            mocked_get.return_value.ok = False

            schedule = self.emp2.monthly_schedule('June')
            mocked_get.assert_called_with('http://company.com/Smith/June')
            self.assertEqual(schedule, 'Bad Response!')

'''

if __name__ == "__main__":
    unittest.main()
