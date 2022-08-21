from convertSetImage import convertSetImage

from getBrowser import getBrowser, waitForNoElement
from time import sleep 
from PIL import Image 

from selenium.webdriver.common.by import By

def setAiMeme():
    browser = getBrowser("https://imgflip.com/ai-meme")

    waitForNoElement(browser, 'site-loading')
    randomButtonEl = browser.find_element(By.ID, "aim-random-btn")
    randomButtonEl.click()
    waitForNoElement(browser, 'site-loading')

    featureElement = browser.find_element(By.XPATH, "//*[@id='aim-preview-wrap']") 
    location = featureElement.location 
    size = featureElement.size 
    browser.save_screenshot("fullPageScreenshot.png") 
    x = location['x'] 
    y = location['y'] 
    w = x + size['width'] 
    h = y + size['height'] - 80
    fullImg = Image.open("fullPageScreenshot.png") 
    cropImg = fullImg.crop((x, y, w, h)) 
    cropImg.save('croppedMeme.png') 
    browser.quit()  

    convertSetImage('croppedMeme.png')

if __name__ == "__main__":
    setMeme()
