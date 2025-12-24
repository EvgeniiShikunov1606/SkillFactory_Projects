from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def get_driver():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver
