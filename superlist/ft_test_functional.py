from unittest import TestCase
from selenium import webdriver


class HomeUserStoryTestCase(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_home_page(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title, 'fail title')

    def tearDown(self):
        self.browser.quit()