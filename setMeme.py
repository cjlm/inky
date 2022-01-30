from convertSetImage import convertSetImage

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


from time import sleep 
from PIL import Image 

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
    
# from selenium.webdriver.firefox.options import Options
# options = Options()
# options.headless = True

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")

# browser = webdriver.Firefox(options=options)    
browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',options=options);

browser.set_window_size(1920, 2000)

browser.get("https://imgflip.com/ai-meme") 

def wait():
    WebDriverWait(browser, 10000).until(EC.invisibility_of_element_located((By.ID, "site-loading")))    

wait()
randomButtonEl = browser.find_element_by_id("aim-random-btn")
randomButtonEl.click()
wait()

featureElement = browser.find_element_by_xpath("//*[@id='aim-preview-wrap']") 
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

