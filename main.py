from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

browser = webdriver.Chrome()
browser.get('https://hh.ru/')
tt = browser.find_element(By.ID, 'a11y-search-input')
tt.send_keys('Python')
button = browser.find_element(By.CSS_SELECTOR, '[data-page-analytics-event="searchButton.submit"]')
button.click()
salary_max = browser.find_element(By.XPATH, '//*[@id="a11y-main-content"]/div[2]/div/div[1]/div[1]/div[3]/span').text
print(re.sub('\D', '', salary_max))
element = WebDriverWait(browser, 20)\
    .until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hh-tab-id="searchVacancy"]')))
print(element.text)
browser.quit()


