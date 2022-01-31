from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import requests

URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22" \
      "%3A%7B%22west%22%3A-122.63417281103516%2C%22east%22%3A-122.23248518896484%2C%22south%22%3A37.64573520729978%2C" \
      "%22north%22%3A37.904621063717464%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B" \
      "%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3A" \
      "false%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%" \
      "22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%" \
      "7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

PATH = "/Users/apple/Desktop/chromedriver"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/97.0.4692.99 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"}

URL_FORM = "https://forms.gle/3PQAWmoVpHEitP66A"


class ScrapeFill:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=PATH)
        self.link = []
        self.price = []
        self.address = []

    def scrape_website(self):
        # This is a function that scrape price, address and link from zillow website

        # getting html elements
        response = requests.get(URL, headers=HEADERS)

        # preparing soup
        soup = BeautifulSoup(response.text, "html.parser")

        # getting items from the website
        address = soup.find_all(name="address")
        price = soup.find_all(name="div", class_="list-card-price")
        link = soup.find_all(name="a", class_="list-card-img")

        # looping through the item to create list for each items
        for num in range(0, len(address)):
            self.address.append(address[num].text)
            self.price.append(price[num].text.split("/")[0].split("+")[0])
            self.link.append(link[num].get("href"))

    def fill_form(self, address, link, price):
        # this is a function that fills the Google form with the details collected from the Google form

        # open browser and visit link
        self.driver.get(URL_FORM)
        time.sleep(4)
        # enter address
        address_input = self.driver.find_element(By.CSS_SELECTOR, ".quantumWizTextinputPaperinputInput.exportInput")
        address_input.send_keys(address)

        # enter property price
        price_input = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div['
                                                         '2]/div/div[1]/div/div[1]/input')
        price_input.send_keys(price)

        # enter link
        link_input = self.driver.find_element(By.XPATH,
                                              '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                              '1]/div/div[1]/input')
        link_input.send_keys(link)

        # click on submit button
        submit_response = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
        submit_response.send_keys(Keys.ENTER)
        time.sleep(4)

        # click to enter the next respoonse
        # another_response = self.driver.find_element(By.LINK_TEXT, "Submit another response")
        # another_response.click()
        # time.sleep(4)
        # time.sleep(20)
