import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns


base_url = "https://www.blocket.se/annonser/norrbotten/fordon/batar/motorbat?cg=1061&f=p&page={page}&q=b%C3%A5tar&r=1&sort=price"

titles = []
prices = []
locations = []
dates = []
page_nums = ['1']
# =============================================== Get Data ===============================================
# Get the ads on a single page
def get_ads_on_page(page_number):
    url = base_url.format(page=page_number)
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    ads = soup.find_all('div', class_='styled__Wrapper-sc-1kpvi4z-0 iQpUlz')
    
    for ad in ads:
        title = ad.find('span', class_='styled__SubjectContainer-sc-1kpvi4z-9 ekmXle').text.strip()
        price = ad.find('div', class_='Price__StyledPrice-sc-1v2maoc-1 lbJRcp').text.strip()
        location = ad.find('p', class_='styled__TopInfoWrapper-sc-1kpvi4z-22 cRXmkf').text.strip()
        
        # Check if the location contains the separator and split accordingly
        if '\xa0·\xa0' in location:
            location = location.split('\xa0·\xa0')[1].strip()
        
        date = ad.find('p', class_='styled__Time-sc-1kpvi4z-18 jMeTyX').text.strip()

        if price > '0':
            titles.append(title)
            prices.append(price)
            locations.append(location)
            dates.append(date)

    # Check if the pagination element exists
    pagination_element = soup.find('div', class_='Pagination__Wrapper-sc-uamu6s-2 dkwcGr')
    if pagination_element:
        page_num = pagination_element.text.strip()
        page_nums.append(page_num)
    else:
        print(f"Pagination element not found on page {page_number}")


def get_last_number_from_list(lst):
    return int(lst[-1][-1])

# Initial range setup
last_number = get_last_number_from_list(page_nums)

# Loop through the pages dynamically
page_number = 1
while page_number <= last_number:
    get_ads_on_page(page_number)
    time.sleep(1)  

    last_number = get_last_number_from_list(page_nums)
    page_number += 1

# print(titles)
# print("")
# print(prices)
# print("")
# print(locations)
# print("")
# print(dates)

# =============================================== Use Data ===============================================

data = pd.DataFrame({
    'Title': titles,
    'Price': prices,
    'Location': locations,
    'Date': dates
})

data.to_csv('blocket_motorbat.csv', index=False)
print("Data saved to blocket_motorbat.csv")

data = pd.read_csv('blocket_motorbat.csv')

data['Price'] = data['Price'].str.replace('kr', '').str.replace(' ', '').astype(float)

# Omvandla årsinformationen till numeriskt format
data['Date'] = pd.to_numeric(data['Date'], errors='coerce')


city_counts = data['Location'].value_counts()


# =============================================== Visualizing ===============================================

plt.figure(figsize=(12, 6))
city_counts.plot(kind='bar')
plt.title('Antal båtar till salu per stad')
plt.xlabel('Stad')
plt.ylabel('Antal båtar')
plt.xticks(rotation=90)
plt.show()