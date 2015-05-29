#!/usr/bin/env python
from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup
import unicodecsv

url = 'https://s3.amazonaws.com/python-at-ire15/death_row/dr_scheduled_executions.html'

r = requests.get(url)

html = r.content

soup = BeautifulSoup(html)

body_text = soup.find("div", id='body')

our_table = body_text.find('table')

headers = our_table.find('tr')
myheaders = []

for th in headers.find_all('th'):
	myheaders.append(th.text)

output_file = 'scheduled.csv'

f = open(output_file,'wb')

w = unicodecsv.writer(f, encoding='utf-8')

w.writerow(myheaders)

for tr in our_table.find_all('tr')[1:]:
    tds = tr.find_all('td')
    date = tds[0].text
    link = tds[1].find('a').get('href')
    last = tds[2].text
    first = tds[3].text
    number = tds[4].text
    dob = tds[5].text
    race = tds[6].text
    indate = tds[7].text
    county = tds[8].text
    rowitems = [date, link, last, first, number, dob, race, indate, county]
    w.writerow(rowitems)

f.close()


