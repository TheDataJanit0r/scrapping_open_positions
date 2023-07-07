name = "Deutsche Bank Crawler"
version = "1.0.0"
description = "Crawling der Stellenangebote der Deutschen Bank"

#importing required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import random
import pandas as pd
from datetime import date
from selenium.webdriver.support.relative_locator import locate_with
from fuzzywuzzy import fuzz
from datetime import date, timedelta
import datetime
import calendar
from datetime import datetime





#################### Creating Proxy Settings with Oxylabs ##########

    


options = webdriver.ChromeOptions()
options.add_argument("--window-size=1200,1000")
options.add_argument("--headless")
driver = webdriver.Chrome(
    ChromeDriverManager().install(), options=options
)

driver.implicitly_wait(220)
url = "https://jobs.dkb.de/job/Berlin-%28Senior%29-Backend-Developer-Java/689045101/"
# driver.maximize_window() #maximize the window
driver.get(url)


time.sleep(random.randint(2, 5))
driver.implicitly_wait(10)
######### Access Shadow DOM to refuse Cookies #########





# Aufgaben = driver.find_element(By.XPATH,"//*[contains(text(), 'Was Dich erwartet')]")

Aufgaben =driver.find_element(By.XPATH,"//*[contains(text(), 'DAS HAST DU')]")
Aufgaben2 =driver.find_element(By.XPATH,"//*[contains(text(), 'DAS KANNST DU')]")
Aufgaben_parent=driver.find_elements(locate_with(By.TAG_NAME, "span").below(Aufgaben).above(Aufgaben2))


print(Aufgaben_parent)



Aufgaben =driver.find_element(By.XPATH,"//*[contains(text(), 'DAS KANNST DU')]")
Aufgaben2 =driver.find_element(By.XPATH,"//*[contains(text(), 'DAS MACHST DU')]")
Aufgaben_parent=driver.find_elements(locate_with(By.TAG_NAME, "span").below(Aufgaben).above(Aufgaben2))


print(Aufgaben_parent)



