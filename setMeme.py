from convertSetImage import convertSetImage

from getBrowser import getBrowser, waitForElement
from time import sleep 
from PIL import Image 

from selenium.webdriver.common.by import By

def setMeme():
    browser = getBrowser("https://imgflip.com/")

    randomButtonEl = browser.find_element(By.ID, "panel-flip")
    randomButtonEl.click()
    waitForElement(browser, 'im')

    featureElement = browser.find_element(By.ID, "im")
    location = featureElement.location 
    size = featureElement.size 
    browser.save_screenshot("fullPageScreenshot.png") 
    x = location['x'] 
    y = location['y'] 
    w = x + size['width'] 
    h = y + size['height'] 
    fullImg = Image.open("fullPageScreenshot.png") 
    cropImg = fullImg.crop((x, y, w, h)) 
    cropImg.save('croppedMeme.png') 
    browser.quit()  

    convertSetImage('croppedMeme.png')

if __name__ == "__main__":
    setMeme()
