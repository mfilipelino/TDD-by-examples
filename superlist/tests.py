from django.test import TestCase
from selenium import webdriver


class HomePageTestCase(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_home(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do' in self.browser.title)

    def tearDown(self):
        self.browser.quit()