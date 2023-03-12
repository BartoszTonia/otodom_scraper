from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver


timeout = 8
options = Options()
options.add_argument('headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # hides DevTools output in console


def run_driver(url):
    print(" >>> driver loading: ", end='')
    service = Service("driver\chromedriver.exe")
    driver = webdriver.Chrome(options=options, service=service)
    driver.get(url)
    print(f'{url}', end='')

    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH, "//*")))
    except TimeoutException as e:
        print(f' >>> Timeout {url} Message: {e}')

    return driver
