import os
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def download_google_images(search_query: str, number_of_images=500) -> None:
    '''Download google images with this function\n
       Takes -> search_query, number_of_images\n
       Returns -> None
    '''
    def scroll_to_bottom():
        '''Scroll to the bottom of the page
        '''
        last_height = driver.execute_script('return document.body.scrollHeight')
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(2)

            new_height = driver.execute_script('return document.body.scrollHeight')
            try:
                element = driver.find_element(
                    by=By.CSS_SELECTOR,
                    value='.YstHxe input'
                )
                element.click()
                time.sleep(2)
            except:
                pass

            if new_height == last_height:
                break

            last_height = new_height

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    url = 'https://images.google.com/'

    driver.get(
        url=url
    )

    box = driver.find_element(
        by=By.XPATH,
        value="//input[contains(@class,'gLFyf gsfi')]"
    )

    box.send_keys(search_query)
    box.send_keys(Keys.ENTER)
    time.sleep(2)

    scroll_to_bottom()
    time.sleep(2)

    img_results = driver.find_elements(
        by=By.XPATH,
        value="//img[contains(@class,'rg_i Q4LuWd')]"
    )

    print(f'Totla images -> {len(img_results)}')

    count = 0

    for img_result in img_results:
        try:
            WebDriverWait(
                driver,
                15
            ).until(
                EC.element_to_be_clickable(
                    img_result
                )
            )
            img_result.click()
            time.sleep(2)

            actual_img = driver.find_element(
                by=By.XPATH,
                value="//img[contains(@class,'n3VNCb')]"
            )

            src = actual_img.get_attribute('src')
            width = actual_img.get_attribute('width')
            height = actual_img.get_attribute('height')

            if 'https://' in src:
                print(src)
                print(width)
                print(height)
            else:
                print('Base 64 in source.')
                print(width)
                print(height)
        except ElementClickInterceptedException as e:
            print(e)
            print('Image is not clickable.')
        
        count += 1
        if count == number_of_images:
            break


cwd = os.getcwd()

tags = open(f'{cwd}/playground/tags.json')
tags = json.load(tags)

tags = tags['tags']

for tag in tags:
    download_google_images(tag, 10)
