import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.blocket.se/annonser/norrbotten/fordon/batar/motorbat?cg=1061&f=p&page={page}&q=b%C3%A5tar&r=1&sort=price"

titles = []
prices = []
locations = []
dates = []
page_nums = ['1']

def get_ads_on_page(page_number):
    url = base_url.format(page=page_number)
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    ads = soup.find_all('div', class_='styled__Wrapper-sc-1kpvi4z-0 iQpUlz')
    
    page_num = soup.find('div', class_='Pagination__Wrapper-sc-uamu6s-2 dkwcGr').text.strip()
    page_nums.append(page_num)
    for ad in ads:
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
        
# Loop through the desired number of pages
def get_last_number_from_list(lst):
    return int(lst[-1][-1])

# Initial range setup
last_number = get_last_number_from_list(page_nums)

# Loop through the pages dynamically
page_number = 1
while page_number <= last_number:
    get_ads_on_page(page_number)
    time.sleep(1)  # Be polite and avoid hitting the server too hard
    
    # Update the last number based on the latest state of the list
    last_number = get_last_number_from_list(page_nums)
    page_number += 1

print(titles)
print("")
print(prices)
print("")
print(locations)
print("")
print(dates)
print("")
print(page_nums)
print(page_number)