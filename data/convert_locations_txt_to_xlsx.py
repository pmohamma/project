# https://stackoverflow.com/questions/45366870/convert-a-lists-in-list-to-a-csv-file-by-python

import pandas as pd

temp = []
with open('trader_joes_location.txt', 'r') as f:
	s = False
	while True:

		line = f.readline()
		if line and line[0].isdigit() and not line.endswith(')'):
			s = True
			temp.append("{}".format(line.strip()))

		elif s:
			temp[-1] += ", {}".format(line.strip())
			s = False

		if not line:
			break

pd.DataFrame(temp).to_csv('trader_joes_raw_location.csv', sep=',', header=None, index=None)


temp = []
with open('nordstrom_locations.txt', 'r') as f:
	while True:

		line = f.readline()
		arr = line.split(" ")

		arr.pop(0)
		arr =  arr[:-1]

		while True:
			if arr and arr[0] and not arr[0][0].isdigit():
				arr.pop(0)
			else:
				break

		if arr:
			temp.append("{}".format(" ".join(arr).strip()))

		if not line:
			break

pd.DataFrame(temp).to_csv('nordstrom_raw_location.csv', sep=',', header=None, index=None)


temp = []
with open('cabelas_location.txt', 'r') as f:
	s = False
	while True:

		line = f.readline()
		if not s and line and line.strip().endswith('PM'):
			s = True

		elif s:
			temp.append("{}".format(line.strip()))
			s = False

		if not line:
			break

pd.DataFrame(temp).to_csv('cabelas_raw_location.csv', sep=',', header=None, index=None)


# https://pythonprogramminglanguage.com/get-links-from-webpage/
# https://stackoverflow.com/questions/27934387/how-to-get-inner-text-value-of-an-html-tag-with-beautifulsoup-bs4
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import time
from w3lib.url import safe_url_string

req = Request("https://www.fandango.com/movie-theaters/cinemark")
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

theater_pages = []
for link in soup.findAll('a'):
	link_str = link.get('href')
	if link_str and 'theater-page' in link_str:
	    theater_pages.append(link_str)

addresses = []
for theater_link in theater_pages:
	try:
		req = Request(theater_link)
		html_page = urlopen(req)
	except:
		continue

	soup = BeautifulSoup(html_page, "lxml")
	for address in soup.findAll('address'):
		addy = address.text.strip()
		addy_len = len(addy)
		for i in range(1, addy_len-1):
			if addy[i].isalpha() and addy[i] == addy[i].upper() and addy[i-1] != " " and addy[i+1] != " ":
				addy = addy[:i] + ', ' + addy[i:]
				break
		addresses.append(addy)
		print(addy)

pd.DataFrame(addresses).to_csv('cinemark_raw_location.csv', sep=',', header=None, index=None)
print(pd.DataFrame(addresses))