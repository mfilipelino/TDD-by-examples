from unittest import TestCase

from selenium import webdriver


class ServerSideTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    # servidor esta de rodando
    def test_run_server(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Django', self.browser.title, 'Servidor não está rodando')

    def tearDown(self):
        self.browser.quit()