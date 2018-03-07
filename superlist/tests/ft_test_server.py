from unittest import TestCase

from selenium import webdriver


# User story: Acessando o site
class ServerSideTest(TestCase):
    def setUp(self):
        # step: 1 open the browser
        self.browser = webdriver.Chrome()

    def test_run_server(self):
        # step 2 open the website
        self.browser.get('http://localhost:8000')
        # step 3 validate title page
        self.assertIn('To-Do', self.browser.title, 'Servidor não está rodando')

    def tearDown(self):
        self.browser.quit()
