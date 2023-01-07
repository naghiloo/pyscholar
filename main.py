import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from decouple import config, Csv

from .functions import send_sms

def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()
    # add the argument and make the browser Headless.
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = "/usr/bin/google-chrome-beta"
    # Instantiate the Webdriver: Mention the executable path of the webdriver you have downloaded
    # For linux/Mac
    # driver = webdriver.Chrome(options = chrome_options)
    # For windows
    driver = webdriver.Chrome(options = chrome_options)
    return driver


def getScholar(driver, user_id):
    # Step 1: Go to pluralsight.com, category section with selected search keyword
    driver.get(f"https://scholar.google.com/citations?user={ user_id }&hl=en")
    # wait for the element to load
    # try:
    #     WebDriverWait(driver, 5).until(lambda s: s.find_element_by_id("gsc_bdy").is_displayed())
    # except TimeoutException:
    #     print("TimeoutException: Element not found")
    #     return None

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")
    # Step 3: Iterate over the search result and fetch the course
    body = soup.find(id='gsc_bdy')
    publications = body.find(id='gsc_a_t')
    citedby = body.find(id='gsc_rsb_st').find_all('tr')[1:-1]

    changes = {
        "publications"  : "",
        "citedby" : "",
        "hindex"   : "",
    }

    # grab citation changes
    for item in citedby:
        changes[item.find('a').find(text=True)] = int(item.find("td", {"class": "gsc_rsb_std"}).find(text=True))

    # grab publications count changes
    changes["publications"] = len(publications.find_all('tr')) - 2

    # close the driver.
    driver.close()
    return changes


# create the driver object.
driver = configure_driver()

while True:
    r = open("result.json", "r")
    res = json.loads(r.read())

    res = {
        "publications": res["publications"],
        "citedby": res["citedby"],
        "hindex": res["hindex"],
    }

    for user_id in config('SCHOLAR_USERS', cast=Csv()):
        changes = getScholar(driver, user_id)

    
    if (res["citedby"] != changes["citedby"]) or (res["hindex"] != changes["hindex"]) or (res["publications"] != changes["publications"]):
        print(send_sms(changes))
        f = open("result.json", "w")
        f.write(json.dumps(changes))
        f.close()
    
    r.close()

    time.sleep(int(config('SLEEP_SECONDS')))
