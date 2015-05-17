import urllib2
from bs4 import BeautifulSoup
from listing_tools import get_type, get_location, is_student, is_pet_ok, lease_type
import re
import copy
from urlparse import urljoin
import logging
import pymongo
import sys

def af_links(url_source):
	# Will return a list of links to individual listings if given the url for a company's Appfolio page
	appfolio_list = urllib2.urlopen(url_source).read()
	soup = BeautifulSoup(appfolio_list)

	getTheLinks = soup.find_all("a", class_="js-link-to-detail")
	linkS = set()

	for link in getTheLinks:
		var = link.get('href')
		linkS.add(urljoin(url_source, var))
	
	return linkS

def af_crawl(listing_URL, origin, special, contact):
	soup = BeautifulSoup(urllib2.urlopen(listing_URL).read())
	soupStrings = soup.find_all(text=True)

	jsonDoc = {}
	jsonDoc["URL"] = listing_URL
	jsonDoc["origin"] = origin
	jsonDoc["title"] = str(soup.find("h1",class_="align_left").string).strip()

	#get rental cost as integer, removing comma if present in value
	try:
		costLoc = soupStrings.index('Rent:')
		cost= soupStrings[costLoc+1].strip()
		costInt = int(cost[1:].replace(',',''))
	except ValueError:
		slash_month = "/mo"
		for string in soupStrings:
			if slash_month in string:
				costInt = int(re.findall('\d+', string)[0])
		else:
			costInt = 0
	if costInt == 0:
		return None
	jsonDoc["cost"] = costInt

	# number of days between payments, 30 = monthly, 7 = weekly etc
	jsonDoc["costType"] = 30

	#get listing location
	locOne = soup.find("div", class_="unit_address").contents
	addressString = locOne.pop().strip()
	jsonDoc["location"] = get_location(addressString)

	full_desc = ""
	desc = soup.find("p",class_="align_left").strings
	for string in desc:
		full_desc = full_desc + string
	jsonDoc["description"] = full_desc.strip()

	jsonDoc["type"] = get_type(jsonDoc["description"])

	#get list of images in listing
	imageObject = soup.find_all("a", class_="highslide")
	imageList = []
	for link in imageObject:
		imageList.append(link.get('href'))
	if imageList == []:
		imageList.append("/static/house.png")
	jsonDoc["images"] = imageList

	#returns list of strings, the listed amenities on the given listing
	true_amenities = []
	amenities = soup.find_all('ul', class_="list")
	for element in amenities:
		for item in element.contents:
			string = item.string
			if string.strip() == '':
				pass
			else:
				true_amenities.append(string)
	jsonDoc["amenities"] = true_amenities

	#get square footage as an integer (0 = unspecified)
	try:
		sqfLoc = soupStrings.index('Square feet:')
		sqf = soupStrings[sqfLoc+1]
		SIZE = int(sqf.replace(',',''))
	except ValueError:
		SIZE = 0
	jsonDoc["sizeSQF"] = SIZE

	#get int for bedrooms and bathrooms * NOTE THIS WILL NOT WORK IF THERE ARE MORE THAN 9 BEDROOMS OR BATHROOMS
	try:
		bedBath = soup.find("div",class_="dark_grey_box").string.strip()
		try:
			bedrooms = int(bedBath[0])
		except ValueError:
			bedrooms = 1
		try:
			slashLoc = bedBath.index('/')
			bathrooms = int(bedBath[slashLoc+2])
		except ValueError:
			bathrooms = 1
	except AttributeError:
		bedrooms = 1
		bathrooms = 0
	jsonDoc["bedrooms"] = bedrooms
	jsonDoc["bathrooms"] = bathrooms

	#get available date as a string
	try:
		availLoc = soupStrings.index('Available:')
		availDate = soupStrings[availLoc+1].strip()
	except ValueError:
		availDate = 0
	jsonDoc["available"] = availDate

	#get application fee as an int
	try:
		aFeeLoc = soupStrings.index('Application Fee:')
		aFee = soupStrings[aFeeLoc+1].strip()
		appFee = int(aFee[1:])
	except ValueError:
		appFee = 0
	jsonDoc["appFee"] = appFee

	#get security deposit as an integer, must remove comma from value to create integer
	try:
		secDepLoc = soupStrings.index('Security Deposit:')
		secDep = soupStrings[secDepLoc+1].strip()
		securityDeposit = int(secDep[1:].replace(',',''))
	except ValueError:
		securityDeposit = 0
	jsonDoc["secDeposit"] = securityDeposit

	jsonDoc["pets"] = is_pet_ok(jsonDoc["description"], jsonDoc["amenities"])

	jsonDoc["lease"] = lease_type(jsonDoc["description"], jsonDoc["amenities"])

	#Does this listing accept Section 8, HACSA
	jsonDoc["special"] = special

	jsonDoc["student"] = is_student(jsonDoc["description"], jsonDoc["title"])

	#Link to Apply if present
	try:
		applyObject = soup.find_all(href=re.compile("rental_applications"))[0]
		applyNow = urljoin(listing_URL, applyObject.get('href'))
	except IndexError:
		applyNow = ''
	jsonDoc["applyNow"] = applyNow

	jsonDoc["contact"] = contact

	return jsonDoc

def af_update_crawl(collection, af_source, origin, special, contact):
	current_list = af_links(af_source) #list of listing urls that are currently posted on the PM's website
	current_DB_list_cursor = collection.find({"origin":origin},{"URL":1}) #cursor for list of dictionaries, where each dict contains the url and object ID for that listing in the DB
	crawl_list = copy.copy(current_list) #list to crawl after it has been modified with only the listings we do not have

	newCount = 0
	removeCount = 0

	current_DB_list = [] #actual list of dict's, where each dict contains the url and obj ID for that listing

	for obj in current_DB_list_cursor: 
		current_DB_list.append(obj)
		if obj["URL"] in crawl_list:
			crawl_list.remove(obj["URL"]) #for each listingin the DB, if it's in the crawl_list too, then remove it

	for listing_obj in current_DB_list: # Removes Listings from DB that are not currently listed on Chinook's Website
		if listing_obj["URL"] in current_list:
			pass
		else:
			removeCount = removeCount + 1
			collection.delete_many({"URL": listing_obj["URL"]}) #using delete_many just to make sure any duplicates are deleted

	# af_crawl(listing_URL, origin, special, contact):
	# May want to use insert_many() **new in mongo 3.0....
	for link in crawl_list:
		try:
			INSERTME = af_crawl(link, origin, special, contact)
			collection.insert_one(INSERTME)
			newCount = newCount + 1
		except:
			print link + "did not work because..."
			print sys.exc_info()
			pass

	print str(newCount) + " added to database for " + origin
	print str(removeCount) + " removed from database for " + origin

