import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

url  = "https://www.blocket.se/annonser/norrbotten/fordon/batar/motorbat?cg=1061&f=p&page=1&q=b%C3%A5tar&r=1&sort=price"
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')
ads = soup.find_all('div', class_='styled__Wrapper-sc-1kpvi4z-0 iQpUlz')

titles = []
prices = []
locations = []
dates = []

def get_ads_on_page():
    for ad in ads:
        print(ad.prettify())
        title = ad.find('span', class_='styled__SubjectContainer-sc-1kpvi4z-9 ekmXle').text.strip()
        price = ad.find('div', class_='Price__StyledPrice-sc-1v2maoc-1 lbJRcp').text.strip()
        location = ad.find('p', class_='styled__TopInfoWrapper-sc-1kpvi4z-22 cRXmkf').text.strip()
        if '\xa0·\xa0' in location:
            location = location.split('\xa0·\xa0')[1].strip()
        date = ad.find('p', class_='styled__Time-sc-1kpvi4z-18 jMeTyX').text.strip()

        titles.append(title)
        prices.append(price)
        locations.append(location)
        dates.append(date)



get_ads_on_page()

print(titles)
print("")
print(prices)
print("")
print(locations)
print("")
print(dates)