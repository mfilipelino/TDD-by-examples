from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

print(browser.name)
print(browser.current_url)

assert 'Django' in browser.title