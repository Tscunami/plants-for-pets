from app import *
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    WebDriverException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from time import sleep

CHROMEDRIVER_PATH = r"C:\Shortcuts\Applications/geckodriver.exe"
COOKIES_AGREE_XPATH = "/html/body/div[2]/div[2]/div[3]/span/div/div/div[3]/button[2]/div"
GOOGLE_SEARCH_XPATH = "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input"
FIRST_ELEMENT_XPATH = "/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/a/h3"
FIRST_ELEMENT_2_XPATH = "/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div[1]/a/h3"
FIRST_ELEMENT_3_XPATH = "/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/a/h3"
SECOND_ELEMENT_XPATH = "/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[1]/a/h3"
SECOND_ELEMENT_2_XPATH = "/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div/div[1]/a/h3"
WIKIPEDIA_NAME_XPATH = "/html/body/div[3]/h1/i"
WIKIPEDIA_NAME_2_XPATH = "/html/body/div[3]/h1"


# Find all names, where is url missing
all_names = [name.latin_name for name in DogPlant.query.filter(DogPlant.image_url == "[]").all()]


# I need to find out, how to go through the whole list just from Caroba name to next
go_from_id = 0
for index in range(len(all_names)):
    if all_names[index] == "Holligold":
        go_from_id = index + 1


for name in all_names[go_from_id:]:
    print(name)

# Use Selenium Driver to search for plant on google and click on first link
driver = webdriver.Firefox(executable_path=CHROMEDRIVER_PATH)

# Open google.com
driver.get("https://www.google.com/")

# Accept cookies
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, COOKIES_AGREE_XPATH))).click()

for name in all_names[go_from_id:]:
    # Open google.com
    driver.get("https://www.google.com/")
    sleep(1.5)

    # Fill information in the search engine and submit
    google_search = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, GOOGLE_SEARCH_XPATH)))
    google_search.send_keys(f"{name} english wikipedia")
    google_search.submit()

    sleep(2.5)
    # Click on the first link or the second
    try:
        driver.find_element_by_xpath(FIRST_ELEMENT_XPATH).click()
    except:
        try:
            driver.find_element_by_xpath(SECOND_ELEMENT_XPATH).click()
        except:
            try:
                driver.find_element_by_xpath(SECOND_ELEMENT_2_XPATH).click()
            except:
                try:
                    driver.find_element_by_xpath(FIRST_ELEMENT_2_XPATH).click()
                except:
                    driver.find_element_by_xpath(FIRST_ELEMENT_3_XPATH).click()

    sleep(1.5)
    # Copy Data from the heading
    try:
        w_name = driver.find_element_by_xpath(WIKIPEDIA_NAME_XPATH).text
    except Exception as e:
        print(f"Error --- {name}")
        print(e)

        try:
            w_name = driver.find_element_by_xpath(WIKIPEDIA_NAME_2_XPATH).text
        except TimeoutException:
            print(f"Error --- {name}")

        else:
            with open("../wrong_names.csv", mode="a", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([name, w_name])
            print("OK repaired")

    else:
        with open("../wrong_names.csv", mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([name, w_name])
        print("OK")
