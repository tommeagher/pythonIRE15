#!/usr/bin/env python
from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup
import unicodecsv

base_url = 'https://s3.amazonaws.com/python-at-ire15/death_row/'

new_page = 'dr_offenders_on_dr.html'

url = base_url + new_page

r = requests.get(url)

html = r.content

soup = BeautifulSoup(html)

body_text = soup.find("div", id='body')

our_table = body_text.find('table')

headers = our_table.find('tr')
myheaders = []

for th in headers.find_all('th'):
	myheaders.append(th.text)

print myheaders

output_file = 'deathrow.csv'

f = open(output_file,'wb')

w = unicodecsv.writer(f, encoding='utf-8')

w.writerow(myheaders)

for tr in our_table.find_all('tr')[1:]:
    tds = tr.find_all('td')
    number = tds[0].text
    link = tds[1].find('a').get('href')
    last = tds[2].text
    first = tds[3].text
    dob = tds[4].text
    gender = tds[5].text
    race = tds[6].text
    indate = tds[7].text
    county = tds[8].text
    offensedate = tds[9]
    rowitems = [number, link, last, first, dob, gender, race, indate, county, offensedate]
    w.writerow(rowitems)

f.close()


