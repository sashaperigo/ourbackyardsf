import re
import requests
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup

def get_updates(url):
    r = requests.get(url)
    b = BeautifulSoup(r.text, "lxml")
    donors = [x for x in b.find_all('div', attrs={'class':'supporter js-donation-content '})][10:]
    name = []
    amount = []
    time = []
    for donor in donors:
        time_text = donor.find('div', attrs={'class':'supporter-time'}).text
        if 'Just' in time_text:
            if donor.find('a', attrs={'class':'supporter-name js-profile-donor'}) != None:
                name.append(donor.find('a', attrs={'class':'supporter-name js-profile-donor'}).text)
            else:
                name.append(donor.find('div', attrs={'class':'supporter-name'}).text)
            amount.append(int(re.sub("[^0-9]", "",donor.find('div', attrs={'class':'supporter-amount'}).text)))
            time.append(date.today())
        elif ('min' in time_text) and (int(re.sub("[^0-9]", "",time_text))<=15):
            if donor.find('a', attrs={'class':'supporter-name js-profile-donor'}) != None:
                name.append(donor.find('a', attrs={'class':'supporter-name js-profile-donor'}).text)
            else:
                name.append(donor.find('div', attrs={'class':'supporter-name'}).text)
            amount.append(int(re.sub("[^0-9]", "",donor.find('div', attrs={'class':'supporter-amount'}).text)))
            time.append(date.today())
    df = pd.DataFrame({'name':name,'amount':amount,'time':time})
    df['url'] = url
    return df

if __name__ == "__main__":
    safe_url = r'https://www.gofundme.com/f/safe-embarcadero-for-all'
    safer_url = r'https://www.gofundme.com/safer-embarcadero-for-all'
    safe_df = get_updates(safe_url)
    safer_df = get_updates(safer_url)
    update = pd.concat([safe_df, safer_df])
    if len(update)>0:
        master = pd.read_csv(r'./data/master_data.csv')
        result = pd.concat([master, update])
        result.reset_index(inplace=True, drop=True)
        result.to_csv(r'./data/master_data.csv', index=False)
