from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver

class ImmoWebUrlScrapper:

    def __init__(self, url, max):
        self.url = url
        self.max = max

    def cooking_soup(self, url_):
        driver = webdriver.Firefox()
        driver.implicitly_wait(3)
        driver.get(url_)

        #element = driver.find_element(by='id', value='uc-btn-accept-banner')
        #element.click()

        soup_file = driver.page_source
        soup = BeautifulSoup(soup_file, 'lxml')
        driver.close()
        return soup
    
    def url_getter(self, soup):
        list_of_urls = []
        first_tags = soup.find_all('li', attrs={'class': 'search-results__item'})
        houses = []
        for tag in first_tags:
            houses += tag.find_all('a', attrs={'class': 'card__title-link'})
        for house in houses:
            list_of_urls.append(house.get('href'))
        return list_of_urls

    def get_next_page(self, soup):
        button = soup.find('ul', attrs={'class': 'pagination'})
        ref = button.find('a', 'pagination__link pagination__link--next button button--text button--size-small')
        if ref:
            return ref.get('href')
        else:
            return None
    
    def all_the_urls(self):
        all_urls = []
        new_url = self.url
        while new_url and (self.max >= len(all_urls)):
            soup = self.cooking_soup(new_url)
            new_url = self.get_next_page(soup)
            list = self.url_getter(soup)
            all_urls += list
        return pd.Series(all_urls)

scrapper = ImmoWebUrlScrapper('https://www.immoweb.be/en/search/duplex/for-sale?countries=BE&page=1&orderBy=relevance', 50)
file = scrapper.all_the_urls()
file.to_csv('urls')


    