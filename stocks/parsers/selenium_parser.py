# Find the financials url of the company on Zonebourse
from asyncio.windows_events import NULL

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_financials_url(company_name):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path="stocks/parsers/chromedriver.exe", options=options)

    driver.get(f"https://www.zonebourse.com/recherche/?q={company_name}")
    driver.implicitly_wait(5)
    iframe = NULL

    try:
        iframe = driver.find_element(By.XPATH, '//*[@id="appconsent"]/iframe')
    except NoSuchElementException:
        iframe = NULL

    if (iframe!=NULL):
        driver.switch_to.frame(iframe)
        accept = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div[1]/button')
        accept.click()
        driver.switch_to.default_content()

    stock_page = driver.find_element(By.XPATH, '//*[@id="advanced-search__instruments"]/div[3]/table/tbody/tr[1]/td[1]/a/span')
    stock_page.click()
    temp = driver.find_elements(By.CLASS_NAME, 'link3')
    for i in temp:
        if i.text == "Finances":
            financials_url = i.get_attribute("href")
            break
    driver.quit()
    
    return financials_url
