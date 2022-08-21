from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

def getBrowser(url):
  options = Options()
  options.add_argument("--headless")

  browser = webdriver.Chrome('/opt/homebrew/bin/chromedriver',options=options);
  browser.set_window_size(1920, 2000)
  browser.get(url)
  
  return browser 

def waitForNoElement(browser, id):
    WebDriverWait(browser, 10000).until(EC.invisibility_of_element_located((By.ID, id)))    

def waitForElement(browser, id):
    WebDriverWait(browser, 10000).until(EC.presence_of_element_located((By.ID, id)))    