
import re
import pandas as pd
from datetime import date, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver

def open_browser(url):
    browser = webdriver.Chrome(r'./chromedriver.exe')
    browser.implicitly_wait(2)
    browser.get(url)
    return browser
    
def scrape_browser(browser):
    html = browser.page_source
    browser.close()
    b = BeautifulSoup(html, "lxml")
    return b

def build_df(b, url):
    donors = [x.find('div', attrs={'class':'column small-10 medium-11'}) for x in b.find_all('div', attrs={'class':'supporter-info'}) if x.find('div', attrs={'class':'column small-10 medium-11'})!=None][10:]
    name = []
    amount = []
    time = []

    for donor in donors:
        if donor.find('a', attrs={'class':'supporter-name js-profile-donor'}) != None:
            name.append(donor.find('a', attrs={'class':'supporter-name js-profile-donor'}).text)
        else:
            name.append(donor.find('div', attrs={'class':'supporter-name'}).text)
        amount.append(int(re.sub("[^0-9]", "",donor.find('div', attrs={'class':'supporter-amount'}).text)))
        if ('hour' in donor.find('div', attrs={'class':'supporter-time'}).text) or ('min' in donor.find('div', attrs={'class':'supporter-time'}).text) or ('Just' in donor.find('div', attrs={'class':'supporter-time'}).text):
            time.append(date.today() - timedelta(days=1))
        else:
            days = int(re.sub("[^0-9]", "",donor.find('div', attrs={'class':'supporter-time'}).text))
            time.append(date.today() - timedelta(days=days + 1))
        
    df = pd.DataFrame({'name':name,'amount':amount,'time':time})
    df['url'] = url
    return df

safe_url = r'https://www.gofundme.com/f/safe-embarcadero-for-all'
browser = open_browser(safe_url)
#PAUSE HERE
b = scrape_browser(browser)
safe_df = build_df(b, safe_url)


safer_url = r'https://www.gofundme.com/safer-embarcadero-for-all'
browser = open_browser(safer_url)
#PAUSE HERE
b = scrape_browser(browser)
safer_df = build_df(b, safer_url)

result = pd.concat([safe_df, safer_df])
result.to_csv(r'./data/master_data.csv', index=False)
