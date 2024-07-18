from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

import os

def scroll_down(driver: webdriver):
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def element_exists(driver:webdriver, by:By, ref:str, time=4, refresh=False):
    ret = False
    try:    # Check si existen más opciones que las del inicio - hacer click en caso de existir
        ret = WebDriverWait(driver, time).until(EC.presence_of_element_located((by,ref)))
        if refresh == True:
            driver.refresh()
        try:
            ret = WebDriverWait(driver, time).until(EC.presence_of_element_located((by,ref)))
        except :
            pass
    except TimeoutException:
        pass
    return ret

def login_linkedin(username, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(ChromeDriverManager().install())#, options=chrome_options)

    # Login
    driver.get("https://www.linkedin.com/uas/login")
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'password')))

    we_email=driver.find_element("id", "username")
    we_email.send_keys(username)
    we_password=driver.find_element("id", "password")
    we_password.send_keys(password)
    we_password.send_keys(Keys.RETURN)
    time.sleep(2)
    
    return driver