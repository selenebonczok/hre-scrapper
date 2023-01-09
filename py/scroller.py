# Some Amnesty sites do not display their outputs page by page. 
# Instead, outputs are revealed as the user scrolls down. In such 
# cases, the main algorithm in wscrapper.py will fail, since it assumes 
# a page-by-page arrangement.

# This script uses Selenium to artificially scroll down a site 
# until all entries are revealed, to only then begin HTML parsing 
# and data extraction. 

from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
import bs4 
import time
import lxml

def make_soup_from_scrolling_site(url, pause_time=1):


    browser = webdriver.Firefox()
    browser.get(url)
    last_height = browser.execute_script("return document.body.scrollHeight")
        
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html = browser.page_source 
    soup = bs4.BeautifulSoup(html, "lxml")
    return soup

make_soup_from_scrolling_site("https://www.amnesty.org.au/?s=", pause_time=4)
