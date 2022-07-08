# %%
from fileinput import filename
from importlib.resources import path
from os import link
from re import search
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from typing import List, Union, Optional
import time
import urllib.request
import os
import json
from sqlalchemy import create_engine
import pandas as pd
import boto3

class Scraper:
    '''
    This class is a scraper that can be used for browsing autotrader

    Parameters
    ----------
    url: str
        The link that we want to visit

    Attribute
    ---------
    driver: 
        This is the webdriver object
    '''
    def __init__(self, url = None):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"')
        if url == None:
            url = 'https://www.autotrader.co.uk'
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) 
        self.driver.get(url)
        # DATABASE_TYPE = 'postgresql'
        # DBAPI = 'psycopg2'
        # HOST = 'june-test.cqsmj26wqota.us-east-1.rds.amazonaws.com'
        # USER = 'postgres'
        # PASSWORD = 'aicore123'
        # DATABASE = 'postgres'
        # PORT = 5432
        key_id = input('Enter your AWS key id: ')
        secret_key = input('Enter your AWS secret: ')
        bucket_name = input('Enter your bucket name: ')
        region = input('Enter your region: ')
        # self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        # self.engine.connect()
        self.client = boto3.client(
            's3',
            aws_access_key_id = key_id,
            aws_secret_access_key = secret_key,
            region_name = region
            )

    def accept_cookies(self, xpath: str = '//button[@title="Accept All"]'):
        '''
        This method looks for and clicks on the accept cookies button

        Parameters
        ----------
        xpath: str
            the xpath of the accept cookies button
        '''
        try:
            time.sleep(2)
            self.driver.switch_to.frame('sp_message_iframe_576092')
            (WebDriverWait(self.driver, 10)
                .until(EC.presence_of_element_located((By.XPATH, xpath))))
            self.driver.find_element(By.XPATH, xpath).click()
            self.driver.switch_to.default_content()
        except TimeoutException:
            print('no cookies found')
            
    def find_postcode(self, xpath: str = '//input[@type="text"]'):
        '''
        This method looks for and clicks on the postcode search bar

        Parameters
        ----------
        xpath: str
            the xpath of the postcode search bar

        Returns
        -------
        Union[webdriver.element, None]
        '''
        try:
            time.sleep(1)
            postcode = (WebDriverWait(self.driver, 10)
                .until(EC.presence_of_element_located((By.XPATH, xpath))))
            postcode.click()
            return postcode
        except TimeoutException:
            print('no postcode found')
            return None

    def enter_postcode(self, text) -> None:
        '''
        This method enters keys into the postcode search bar

        Parameters
        ----------
        text: str
            The keys we want to pass into the postcode search bar
        '''
        postcode = self.find_postcode()
        if postcode:
            postcode.send_keys(text)
        else:
            raise Exception('No postcode found')

    def choose_distance(self, xpath: str = '//select[@id="distance"]'):
        '''
        This method looks for and clicks on the distance drop-down list

        Parameters
        ----------
        xpath: str
            the xpath of the distance drop-down list

        Returns
        -------
        Union[webdriver.element, None]
        '''
        try:
            time.sleep(1)
            distance = (WebDriverWait(self.driver, 10)
               .until(EC.presence_of_element_located((By.XPATH, xpath))))
            distance.click()
            return distance
        except TimeoutException:
            print('no distance found')
            return None

    def choose_make(self, xpath: str = '//select[@id="make"]'):
        '''
        This method looks for and clicks on the make drop-down list

        Parameters
        ----------
        xpath: str
            the xpath of the make drop-down list

        Returns
        -------
        Union[webdriver.element, None]
        '''
        try:
            time.sleep(1)
            make = (WebDriverWait(self.driver, 10)
                .until(EC.presence_of_element_located((By.XPATH, xpath))))
            make.click()
            return make
        except TimeoutException:
            print('no make found')
            return None

    def choose_model(self, xpath: str = '//select[@id="model"]'):
        '''
        This method looks for and clicks on the model drop-down list

        Parameters
        ----------
        xpath: str
            the xpath of the model drop-down list

        Returns
        -------
        Union[webdriver.element, None]
        '''
        try:
            time.sleep(1)
            model = (WebDriverWait(self.driver, 10)
                .until(EC.presence_of_element_located((By.XPATH, xpath))))
            model.click()
            return model
        except TimeoutException:
            print('no model found')
            return None
    
    def select_cash(self, xpath: str = '//label[@for="price-type-0"]'):
        '''
        This method looks for and clicks on the cash button

        Parameters
        ----------
        xpath: str
            the xpath of the cash button

        Returns
        -------
        Union[webdriver.element, None]
        '''
        try:
            time.sleep(1)
            cash = (WebDriverWait(self.driver, 10)
                .until(EC.presence_of_element_located((By.XPATH, xpath))))
            cash.click()
            return cash
        except TimeoutException:
            print('no cash found')
            return None

    def select_finance(self, xpath: str = '//label[@for="price-type-1"]'):
        '''
        This method looks for and clicks on the finance button

        Parameters
        ----------
        xpath: str
            the xpath of the finance button

        Returns
        -------
        Union[webdriver.element, None]
        '''
        try:
            time.sleep(1)
            finance = (WebDriverWait(self.driver, 10)
                .until(EC.presence_of_element_located((By.XPATH, xpath))))
            finance.click()
            return finance
        except TimeoutException:
            print('no finance found')
            return None

    def choose_minprice(self, xpath: str = '//select[@id="minPrice"]'):
        '''
        This method looks for and clicks on the min price drop-down list

        Parameters
        ----------
        xpath: str
            the xpath of the min price drop-down list

        Returns
        -------
        Union[webdriver.element, None]
        '''
        try:
            time.sleep(1)
            minprice = (WebDriverWait(self.driver, 10)
                .until(EC.presence_of_element_located((By.XPATH, xpath))))
            minprice.click()
            return minprice
        except TimeoutException:
            print('no model found')
            return None

    def choose_maxprice(self, xpath: str = '//select[@id="maxPrice"]'):
        '''
        This method looks for and clicks on the max price drop-down list

        Parameters
        ----------
        xpath: str
            the xpath of the max price drop-down list

        Returns
        -------
        Union[webdriver.element, None]
        '''
        try:
            time.sleep(1)
            maxprice = (WebDriverWait(self.driver, 10)
                .until(EC.presence_of_element_located((By.XPATH, xpath))))
            maxprice.click()
            return maxprice
        except TimeoutException:
            print('no model found')
            return None

    def enter_search(self, xpath: str = '//button[@type="submit"]') -> None:
        '''
        This method looks for and clicks on the search button

        Parameters
        ----------
        xpath: str
            the xpath of the search button
        '''
        try:    
            time.sleep(1)
            search = (WebDriverWait(self.driver, 10)
                .until(EC.presence_of_element_located((By.XPATH, xpath))))
            search.click()
        except TimeoutException:
            print('no search found')

    def return_links(self, xpath: str = '//div[@class="js-search-results"]//li[@class="search-page__result"]//a[@class="js-click-handler listing-fpa-link tracking-standard-link"]'):
        '''
        This method returns a list of links to the cars on the webpage

        Parameters
        ----------
        xpath: str
            the xpath of the url link to each car
        '''
        container = self.driver.find_elements(By.XPATH, xpath)
        self.link_list = []
        for link in container:
            self.link_list.append(link.get_attribute('href'))
        print(self.link_list)

    def extract_data(self):
        '''
        This method extrats the necassry data from a signle details page

        Parameters
        ----------
        xpath: str
            the xpaths of the details required data
        '''
        # path1 = os.path.join('/Users/mosesomiteru/Documents/AiCore Stuff', 'raw_data')
        # os.mkdir(path1)
        
        self.car_dict = {
                    'Link': [],
                    'ID': [],
                    'Name': [],
                    'Year': [],
                    'Price': [],
                    'Mileage': [],
                    }             

        # self.df_cars = pd.DataFrame(self.car_dict)
        # self.df_cars.to_sql('cars', self.engine, if_exists='append')
        self.df_cars = pd.read_sql('cars', self.engine)
        self.id_scraped = list(self.df_cars['ID'])
        
        for link1 in self.link_list[0:5]:
            car_dict_single = {
                               'Link': [],
                               'Name': [],
                               'ID': [],
                               'Year': [],
                               'Price': [],
                               'Mileage': [],
                               }

            id = link1[slice(41, 56)]
            if id in self.id_scraped:
                continue
            else:
                self.driver.get(link1)
                time.sleep(1)
                self.car_dict['Link'].append(link1)
                car_dict_single['Link'].append(link1)
                name_class = self.driver.find_element(By.XPATH, '//h1[@data-testid="advert-title"]').get_attribute('class')
                name = self.driver.find_element(By.XPATH, f'//h1[@class="{name_class}"]')
                self.car_dict['Name'].append(name.text)
                car_dict_single['Name'].append(name.text)
                self.car_dict['ID'].append(id)
                car_dict_single['ID'].append(id)
                class_values = self.driver.find_elements(By.XPATH, '//p')
                class_list = []
                for year_class in class_values:
                    class_list.append(year_class.get_attribute('class'))
                year = self.driver.find_element(By.XPATH, f'//p[@class="{class_list[4]}"]')
                self.car_dict['Year'].append(year.text)
                car_dict_single['Year'].append(year.text)
                price_class = self.driver.find_element(By.XPATH, '//h2[@data-testid="advert-price"]').get_attribute('class')
                price = self.driver.find_element(By.XPATH, f'//h2[@class="{price_class}"]')
                self.car_dict['Price'].append(price.text)
                car_dict_single['Price'].append(price.text)
                mileage_class = self.driver.find_element(By.XPATH, '//span[@data-testid="mileage"]').get_attribute('class')
                mileage = self.driver.find_element(By.XPATH, f'//span[@class="{mileage_class}"]')
                self.car_dict['Mileage'].append(mileage.text)
                car_dict_single['Mileage'].append(mileage.text)
            
            path2 = os.path.join('/Users/mosesomiteru/Documents/AiCore Stuff/raw_data', id)
            os.mkdir(path2) 
            with open(f'/Users/mosesomiteru/Documents/AiCore Stuff/raw_data/{id}/data.json', 'w') as fp:
                json.dump(car_dict_single, fp)

            # self.client.upload_file(f'/Users/mosesomiteru/Documents/AiCore Stuff/raw_data/{id}/data.json', 'june-bucket-test', f'{id}.json')

        self.df_cars = pd.DataFrame(self.car_dict)
        self.df_cars.to_sql('cars', self.engine, if_exists='append')

    def download_images(self):
        '''
        This method downloads the images of the item from a signle details page

        Parameters
        ----------
        xpath: str
            the xpaths of the images on the page
        '''
        for link1 in self.link_list[0:5]:
            id = link1[slice(41, 56)]
            if id in self.id_scraped:
                continue
            else:
                path3 = os.path.join(f'/Users/mosesomiteru/Documents/AiCore Stuff/raw_data/{id}', 'images')
                os.mkdir(path3)
                
                self.driver.get(link1)
                time.sleep(1)
                container1 = self.driver.find_elements(By.XPATH, '//li[@class="sc-fTZpSt bcvdhv"]//img')
                self.image_list = []
                for image in container1:
                    self.image_list.append(image.get_attribute('src'))
                    image_index = self.image_list.index(str(image.get_attribute('src')))
                    filename = f'{image_index}.jpg'
                    full_path = f'/Users/mosesomiteru/Documents/AiCore Stuff/raw_data/{id}/images/{filename}'
                    image_url = image.get_attribute('src')
                    urllib.request.urlretrieve(image_url, full_path)
                
                # self.client.upload_file(f'/Users/mosesomiteru/Documents/AiCore Stuff/raw_data/{id}/images/{image_index}.jpg', 'june-bucket-test', f'{id}-{image_index}.jpg')

if __name__ == '__main__':
    bot = Scraper()
    bot.accept_cookies()
    # bot.find_postcode()
    bot.enter_postcode('B296NL')
    # bot.choose_distance()
    # bot.select_cash()
    # bot.select_finance()
    bot.enter_search()
    bot.return_links()
    # bot.extract_data()
    # bot.download_images()
# %%
