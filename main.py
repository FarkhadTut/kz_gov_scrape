from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import sys
import time

URL = 'https://www.gov.kz/'






class Browser(webdriver.Chrome):
    def __init__(self, base_url, wait=10):
        super().__init__()
        self.base_url = base_url
        self.wait = wait
        self.actions = ActionChains(self)
        self.cur_pos = 0

    def find_and_click(self, xpath):
        element = WebDriverWait(self, self.wait).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        self.click(element)
    
    def click(self, element):
        if not self.is_clickable(element):
            distance_y = int(element.rect['y'] - self.cur_pos)
            self.actions.scroll_by_amount(0, distance_y).perform()
            self.cur_pos += distance_y
            time.sleep(0.5)
        self.actions.click(element)
        self.actions.perform()

    def get_list_of_elements(self, xpath=None, by_class=None, by_tagname=None, by_xpath=None):
        if not xpath is None:
            master_element = WebDriverWait(self, self.wait).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        if not by_class is None:
            elements = self.find_elements(By.CSS_SELECTOR, by_class)
        elif not by_tagname is None:
            elements = self.find_elements(By.TAG_NAME, by_tagname)
        elif not by_xpath is None:
            elements = self.find_elements(By.XPATH, by_xpath)
        
        return elements
        

        
    def get_url(self, wait_xpath):
        self.get(self.base_url)
        WebDriverWait(self, self.wait).until(
            EC.presence_of_element_located((By.XPATH, wait_xpath))
        )
    
    def find_page_element(self, xpath):
        element = WebDriverWait(self, self.wait).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element

    def is_clickable(self, element):
        window_height = self.get_window_size()['height']
        mid_screen = int(window_height/2)
        element_y = element.rect['y'] + int(element.rect['height']/2)
        if element_y < mid_screen:
            return True
        return False




browser = Browser(URL)
STRUC_URL = 'https://www.gov.kz/memleket/entities/{link}/about/structure?lang=ru'


def structure_url(link):
    return STRUC_URL.format(link=link)

####### MINISTRIES ###############
def get_ministries():
    browser.get_url(wait_xpath='/html/body/div/header/div/div/div/div[1]/button/span')
    time.sleep(2)
    browser.find_and_click('/html/body/div/header/div/div/div/div[1]/button/span')
    ministry_elements = browser.get_list_of_elements('/html/body/div/header/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[2]', 
                                                by_class='.catalog-option__content__list-item')

    ministries = []
    for ministry in ministry_elements:
        browser.click(ministry)
        element = browser.find_page_element('/html/body/div/header/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/div/a[2]')
        link = element.get_attribute('href')
        link = link.split('/')[-1]
        ministries.append(link)

    print("SUCESS MINISTRIES:", len(ministries))
    
    return ministries



####### AKIMATS ###############
def get_akimats():
    browser.get_url(wait_xpath='/html/body/div/header/div/div/div/div[1]/button/span')
    time.sleep(2)
    browser.find_and_click('/html/body/div/header/div/div/div/div[1]/button/span')
    browser.find_and_click('/html/body/div/header/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[1]/button[2]')
    akimat_elements = browser.get_list_of_elements('/html/body/div/header/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[2]', 
                                                by_class='.catalog-option__content__list-item')

    akimats = []
    for akimat in akimat_elements:
        browser.click(akimat)
        element = browser.find_page_element('/html/body/div/header/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/div/a[2]')
        link = element.get_attribute('href')
        link = link.split('/')[-1]
        akimats.append(link)


    print("SUCESS AKIMATS:", len(akimats))
    
    return akimats






####### OTHERS ###############
def get_others():
    browser.get_url(wait_xpath='/html/body/div/header/div/div/div/div[1]/button/span')
    time.sleep(2)
    browser.find_and_click('/html/body/div/header/div/div/div/div[1]/button/span')
    browser.find_and_click('/html/body/div/header/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/button[3]')
    other_elements = browser.get_list_of_elements('/html/body/div/header/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[2]', 
                                                by_class='.catalog-option__content__list-item')

    others = []
    print(len(other_elements))
    for other in other_elements:
        temp_dict = {}
        name = other.text.strip()
        if name == 'Ревизионные комиссии':
            browser.click(other)
            other_elements = browser.get_list_of_elements('/html/body/div[1]/main/div/section/div[2]', 
                                                by_xpath='//div[@class="inner-html"]//p')
            for e in other_elements:
                name = e.text.strip()
                link = e.get_attribute('href')
                link = link.split('/')[-1]
                temp_dict['link'] = link
                temp_dict['name'] = name
                others.append(temp_dict)
        else:
            browser.click(other)
            element = browser.find_page_element('/html/body/div/header/div/div/div/div[1]/div/div[1]/div[2]/div[2]/div/div/a[2]')
            link = element.get_attribute('href')
            link = link.split('/')[-1]
            temp_dict['link'] = link
            temp_dict['name'] = name

            others.append(temp_dict)

    print("SUCESS OTHERS:", len(others))

    return others

####### MASLIHATS ###############

def get_maslihats():
    browser.get_url(wait_xpath='/html/body/div/header/div/div/div/div[1]/button/span')
    time.sleep(2)
    browser.find_and_click('/html/body/div/header/div/div/div/div[1]/button/span')
    browser.find_and_click('/html/body/div/header/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[1]/a')
    maslihat_elements = browser.get_list_of_elements('/html/body/div/main/div/section/div[2]/div/div/div',
                                            by_class='.ant-collapse-item')
    maslihats = []
    for maslihat in maslihat_elements:
        browser.click(maslihat)
        time.sleep(0.5)


    maslihat_links = browser.get_list_of_elements(xpath='/html/body/div[1]/main/div/section/div[2]/div/div/div', by_xpath='//div[@class="bvi-tts"]//a')
    for link in maslihat_links:
        temp_dict = {}
        name = link.text.strip()
        maslihat_link = link.get_attribute('href')
        maslihat_link = maslihat_link.strip('/')[-1]
        temp_dict['name'] = name
        temp_dict['link'] = maslihat_link

        # if 'https://www.gov.kz/memleket/entities/' in maslihat_link and not 'documents' in maslihat_link:
        maslihats.append(maslihat_link)
        
    print("SUCESS MASLIHATS:", len(maslihats))

    return maslihats





def main(*args, **kwargs):
    all_links = []
    all_links += get_ministries()
    all_links += get_akimats()
    all_links += get_others()
    all_links += get_maslihats()

    print(len(all_links))

if __name__ == '__main__':
    main()