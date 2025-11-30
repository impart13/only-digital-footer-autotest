"""
Проверка наличия футера и нескольких элементов в нём на страницах сайта https://only.digital/
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

PAGES_TO_TEST = [
    "https://only.digital/",
    "https://only.digital/company",
    "https://only.digital/fields", 
    "https://only.digital/job",
    "https://only.digital/blog",
    "https://only.digital/contacts"
]
    
class TestFooterMultiplePages:
    
    @pytest.fixture(scope="class")
    def driver(self):
        driver = webdriver.Chrome()
        yield driver
        driver.quit()
    
    #Проверка наличия футера на странице и наличия элементов в нем
    @pytest.mark.parametrize("url", PAGES_TO_TEST)
    def test_footer_presence_on_page(self, driver, url):
        driver.get(url)
        time.sleep(4)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        footer = driver.find_element(By.TAG_NAME, "footer")
        assert footer.is_displayed(), f"Футер не отображается на странице {url}"
        
        footer_text = footer.text.strip()
        assert len(footer_text) > 0, f"Футер пустой на странице {url}"
        
        footer_elements = footer.find_elements(By.CSS_SELECTOR, "*")
        assert len(footer_elements) > 1, f"Футер не содержит элементов на странице {url}"
    
    #Проверка элементов футера на страницах
    @pytest.mark.parametrize("url", PAGES_TO_TEST) 
    def test_footer_key_elements_on_page(self, driver, url):
        driver.get(url)
        time.sleep(4)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        footer = driver.find_element(By.TAG_NAME, "footer")
        
        footer_elements = {
            "Лого": "svg.Footer_logo__2QEhf",
            "Соц.сети": ".Socials_socialsWrap__DPtp_",
            "Telegram": ".Telegram_telegramWrap__USZkq",
            "Контактная информация": ".ContactsLinks_contactLinks__vex86",
            "Копирайт+год": ".Footer_year__nyNCc"
        }
        
        missing_elements = []
        for selector_name, selector in footer_elements.items():
            try:
                element = footer.find_element(By.CSS_SELECTOR, selector)
                if not element.is_displayed():
                    missing_elements.append(selector_name)
            except:
                missing_elements.append(selector_name)
        
        assert len(missing_elements) == 0, \
            f"Не обнаружены элементы: {', '.join(missing_elements)}"