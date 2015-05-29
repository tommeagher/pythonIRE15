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

myheaders.extend(['occupation','record'])

#print myheaders

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

    if link.endswith('html'):
        newreq = requests.get(base_url+link)
        newsoup = BeautifulSoup(newreq.content)
        body = newsoup.find(id='body')
        hr = body.find('hr')
        graf = hr.find_next('p')
        try: 
            occupation = graf.text.split(':')[1].strip()
        except:
            try:
                occupation = graf.text.split('\r\n')[1].strip()
            except:
                occupation = ''
        try:
            record = graf.find_next('p').text.split(':')[1].strip()
        except:
            try: 
                record = graf.find_next('p').text.split('\r\n')[1].strip()
            except:
                record = 'None'
    else:
    	occupation = 'Look in JPG'
    	record = 'Look in JPG'

    rowitems = [number, link, last, first, dob, gender, race, indate, county, offensedate, occupation, record]
    w.writerow(rowitems)

f.close()