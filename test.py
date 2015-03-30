import json
from bs4 import BeautifulSoup
import re
import urllib2
import pymongo
import copy
from pprint import pprint
#from listing_tools import zip_city_OR, zip_county_OR, zip_list_OR

link = "https://bell.appfolio.com/listings/listings/04401a04-8e5c-4570-80c1-4db384cbd37f"

#soup = BeautifulSoup(urllib2.urlopen(link).read())
#soupStrings = soup.find_all(text=True)

soup = BeautifulSoup(urllib2.urlopen(link).read())
soupStrings = soup.find_all(text=True)

full_desc = ""
desc = soup.find("p",class_="align_left").strings
count = 0
for string in desc:
	count = count + 1
	if count < 2:
		full_desc = full_desc + string
	else:
		full_desc = full_desc + '<br>' + string

print full_desc.strip()

#jsonDoc["description"] = soup.find("p",class_="align_left").string.strip()


#pprint(soupStrings)

# Studio, Apartment, Condo, Home, else home