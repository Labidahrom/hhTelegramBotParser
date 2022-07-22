from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

browser = webdriver.Chrome()
browser.maximize_window()


def search_for_element(selector):
    element = WebDriverWait(browser, 20).until(EC.presence_of_element_located(selector))
    return element


browser.get('https://hh.ru/')
change_city_link = search_for_element((By.CLASS_NAME, 'supernova-navi-item_area-switcher-button'))
change_city_link.click()
find_city_field = search_for_element((By.CLASS_NAME, 'HH-AreaSwitcherSearch-Input'))
city = 'Великий Новгород'
find_city_field.send_keys(city)
choose_city = search_for_element((By.CSS_SELECTOR, '.area-switcher-autocomplete-item .bloko-text.bloko-text_strong'))
choose_city.click()
vacancy_search = search_for_element((By.ID, 'a11y-search-input'))
vacancy_name = 'бухгалтер'
vacancy_search.send_keys(vacancy_name)
button_search = search_for_element((By.CSS_SELECTOR, '[data-page-analytics-event="searchButton.submit"]'))
button_search.click()
salar = browser.find_elements(By.CSS_SELECTOR, '.bloko-radio__text [data-qa="serp__novafilter-title"]')
time.sleep(2)
vacancy_amount = search_for_element((By.CSS_SELECTOR, '[data-qa="vacancies-total-found"] span'))
vacancy_amount = vacancy_amount.text.replace(', ', '')

solar_list = []
for i in salar:
    if 'от' in i.text:
        some = i.text
        dig = []
        for f in some:
            if f.isdigit():
                dig.append(f)
            numnumm = ''.join(dig)
        solar_list.append(numnumm)

sr_count = browser.find_elements(By.CSS_SELECTOR, '.bloko-radio [name="salary"] + span .bloko-text.bloko-text_tertiary')
total_amount = 0
quantaty = 0
for i in range(len(sr_count)):
    total_amount += int(solar_list[i]) * int(sr_count[i].text)
    quantaty += int(sr_count[i].text)
print('Вы искали ', vacancy_name, 'в городе: ', city)
print('Средняя зарплата по вашей вакансии составляет: ', int(total_amount/quantaty))
print('Найдено: ', vacancy_amount)



