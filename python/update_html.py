#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 00:09:52 2019

@author: adam.raveret
"""

import boto3
import botocore
import pandas as pd
from bs4 import BeautifulSoup


path = r'./data/master_data.csv'
df = pd.read_csv(path)

safe_raised = str(df.groupby('url')['amount'].sum()['https://www.gofundme.com/f/safe-embarcadero-for-all'])
safe_donors = str(df.groupby('url')['url'].count()['https://www.gofundme.com/f/safe-embarcadero-for-all'])
safe_median = str(df[df['url']=='https://www.gofundme.com/f/safe-embarcadero-for-all'].sort_values(by='amount').reset_index(drop=True).loc[round(int(safe_donors)/2),'amount'])
safe_under = str(len(df[(df['url']=='https://www.gofundme.com/f/safe-embarcadero-for-all')&(df['amount']<=100)]))
safer_raised = str(df.groupby('url')['amount'].sum()['https://www.gofundme.com/safer-embarcadero-for-all'])
safer_donors = str(df.groupby('url')['url'].count()['https://www.gofundme.com/safer-embarcadero-for-all'])
safer_median = str(df[df['url']=='https://www.gofundme.com/safer-embarcadero-for-all'].sort_values(by='amount').reset_index(drop=True).loc[round(int(safe_donors)/2),'amount'])
safer_under = str(len(df[(df['url']=='https://www.gofundme.com/safer-embarcadero-for-all')&(df['amount']<=100)]))

dct = {
       'safe-raised':''.join(['$', safe_raised[:-3], ',', safe_raised[-3:]]),
       'safe-donors':safe_donors,
       'safe-median':''.join(['$',safe_median]),
       'safe-under':safe_under,
       'safer-raised':''.join(['$', safer_raised[:-3], ',', safer_raised[-3:]]),
       'safer-donors':''.join([safer_donors[:-3],',',safer_donors[-3:]]),
       'safer-median':''.join(['$',safer_median]),
       'safer-under':''.join([safer_under[:-3],',',safer_under[-3:]])
       }


url = r'./index.html'
with open(url) as f:
    html = f.read() 
    
b = BeautifulSoup(html)

def update_html(key, value):
    b.find('h3', attrs={'id':key}).string.replace_with(value)

for item in dct.keys():
    update_html(item, dct[item])

with open(url, "w") as file:
    file.write(str(b))

BUCKET_NAME = 'ourbackyardsf.com' # replace with your bucket name
KEY = 'index.html' # replace with your object key

s3 = boto3.client('s3')
s3.upload_file(KEY, BUCKET_NAME, 'index.html')
