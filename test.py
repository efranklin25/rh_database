import json
from bs4 import BeautifulSoup
import re
import urllib2
import pymongo
import copy
from pprint import pprint
from urlparse import urlparse



#soup = BeautifulSoup(urllib2.urlopen("http://ipmg-inc.com/").read())

x = urllib2.urlopen("https://webreq.propertyware.com/pw/marketing/website.do?sid=39944208&wid=39485458&forSale=false&action=l&pageNumber=0&callback=loadListCallback&noCacheIE=1431725175889").read()

y = x[x.find('{'):x.rfind('}')+1].replace('\\>','>')

yay = json.loads(y)
pprint(yay)