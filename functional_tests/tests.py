import time
import pytest
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


@pytest.fixture
def browser():
    b = webdriver.Chrome()
    yield b
    b.quit()


def wait_for_row_in_list_table(browser, row_text):
    start_time = time.time()
    while True:
        try:
            table = browser.find_element_by_id('id_list_table')
            rows = table.find_elements_by_tag_name('tr')
            assert row_text in [row.text for row in rows]
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)


def insert_item_in_list(browser, text_item, inputbox_id):
    inputbox = browser.find_element_by_id(inputbox_id)
    inputbox.send_keys(text_item)
    inputbox.send_keys(Keys.ENTER)


def test_can_start_a_list_and_retrieve_it_later(browser, live_server):
    browser.get(live_server.url)
    assert 'To-Do' in browser.title

    header_text = browser.find_element_by_tag_name('h1').text
    assert 'To-Do' in header_text

    inputbox = browser.find_element_by_id('id_new_item')
    assert inputbox.get_attribute('placeholder') == 'Enter a to-do item'

    inputbox.send_keys('Buy peacock feathers')
    inputbox.send_keys(Keys.ENTER)

    inputbox = browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Use peacock feathers to make a fly')
    inputbox.send_keys(Keys.ENTER)

    wait_for_row_in_list_table(browser, 'Use peacock feathers to make a fly')
    wait_for_row_in_list_table(browser, 'Buy peacock feathers')


def test_multiple_user_can_start_lists_at_different_urls(browser, live_server):

    # edith acessa o site e adiciona um elemento na lista
    browser.get(live_server.url)
    inputbox = browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Buy peacock feathers')
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, 'Buy peacock feathers')
    edith_list_url = browser.current_url
    assert re.search('/lists/.+', edith_list_url)

    # reiniciar o browser para não pegar cookies
    # TODO: This part of the test needs rethinking.
    # A new browser instance should be used for a new user.
    # This might require parameterizing the test or using a different approach.
    # For now, we'll keep the existing logic but acknowledge it's not ideal.
    browser.quit()
    browser = webdriver.Chrome()

    # Francis acessa a pagina inicial não tem sinal nenhuma da list de edith
    browser.get(live_server.url)
    page_text = browser.find_element_by_tag_name('body').text
    assert 'Buy peacock feathers' not in page_text
    assert 'make a fly' not in page_text

    # Francis inicia uma nova lista inserindo um item novo
    insert_item_in_list(browser, text_item='Buy milk', inputbox_id='id_new_item')
    wait_for_row_in_list_table(browser, 'Buy milk')

    francis_list_url = browser.current_url
    assert re.search('/lists/.+', francis_list_url)

    assert francis_list_url != edith_list_url

    page_text = browser.find_element_by_tag_name('body').text
    assert 'Buy peacock feathers' not in page_text
    assert 'Buy milk' in page_text
