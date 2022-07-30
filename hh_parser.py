from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests


class HHParser:
    first_vacancy_link =''

    def hhparser(vacancy_name, city):
        def search_for_element(selector):
            element = WebDriverWait(browser, 20).until(EC.presence_of_element_located(selector))
            return element
        browser = webdriver.Chrome()
        browser.maximize_window()
        browser.get('https://hh.ru/')
        change_city_link = search_for_element((By.CLASS_NAME, 'supernova-navi-item_area-switcher-button'))
        change_city_link.click()
        find_city_field = search_for_element((By.CLASS_NAME, 'HH-AreaSwitcherSearch-Input'))
        find_city_field.send_keys(city)
        time.sleep(1)
        city_search_suggestion = browser.find_elements(By.CSS_SELECTOR, '.area-switcher-autocomplete-item')
        if len(city_search_suggestion) < 1:
            return "Не найден город"
        time.sleep(1)
        choose_city_link = search_for_element((By.CSS_SELECTOR, '.area-switcher-autocomplete-item .bloko-text.bloko-text_strong'))
        choose_city_link.click()
        time.sleep(2)
        search_vacancy_field = search_for_element((By.ID, 'a11y-search-input'))
        search_vacancy_field.send_keys(vacancy_name)
        time.sleep(1)
        search_vacancy_button = search_for_element((By.CSS_SELECTOR, '[data-page-analytics-event="searchButton.submit"]'))
        search_vacancy_button.click()
        salary_block = browser.find_elements(By.CSS_SELECTOR, '.bloko-radio__text [data-qa="serp__novafilter-title"]')
        time.sleep(1)
        vacancy_amount_element = browser.find_elements(By.CSS_SELECTOR, '[data-qa="vacancies-total-found"] span')
        if len(vacancy_amount_element) < 1:
            return "Не найдено результатов"
        vacancy_amount = vacancy_amount_element[0].text.replace(', ', '')
        time.sleep(1)
        salary_list = [''.join([f for f in i.text if f.isdigit()]) for i in salary_block if 'от' in i.text]
        time.sleep(1)
        sr_count = browser.find_elements(By.CSS_SELECTOR,
                                         '.bloko-radio [name="salary"] + span .bloko-text.bloko-text_tertiary')
        total_amount = 0
        quantity = 0
        for i in range(len(sr_count)):
            total_amount += int(salary_list[i]) * int(sr_count[i].text)
            quantity += int(sr_count[i].text)
        if salary_list:
            average_salary = int(total_amount / quantity)
        else:
            average_salary = 'Нет данных'
        first_vacancy_element = browser.find_elements(By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy-title"]')[0]
        global first_vacancy_link
        first_vacancy_link = first_vacancy_element.get_attribute('href')
        return vacancy_amount, average_salary, first_vacancy_link
        browser.quit()


    def get_first_vacancy(link):
        browser = webdriver.Chrome()
        browser.get(link)
        time.sleep(1)
        vacancy_description = []
        vacancy_description.append(browser.find_element(By.CSS_SELECTOR, '.vacancy-title').text)
        vacancy_description.append(browser.find_element(By.CSS_SELECTOR, '[data-qa="vacancy-salary"]').text)
        vacancy_item = browser.find_elements(By.CSS_SELECTOR, 'p.vacancy-description-list-item')
        vacancy_item_list = []
        for i in vacancy_item:
            vacancy_item_list.append(i.text)
        join_vacancy_item_list = '\n'.join(vacancy_item_list)
        vacancy_description.append(join_vacancy_item_list)
        vacancy_description.append(browser.find_element(By.CSS_SELECTOR, 'div.vacancy-description').text)
        full_vacancy_description = '\n'.join(vacancy_description)
        return full_vacancy_description
        browser.quit()


# print(HHParser.hhparser('юрист', 'Тула'))
# print(HHParser.get_first_vacancy('https://tula.hh.ru/vacancy/68137561'))



