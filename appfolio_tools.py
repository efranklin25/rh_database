import urllib2
from bs4 import BeautifulSoup
from listing_tools import get_type, get_location, is_student, is_pet_ok, lease_type
import re
import copy
from urlparse import urljoin
import logging
import pymongo

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
	jsonDoc["_id"] = listing_URL
	jsonDoc["origin"] = origin
	jsonDoc["title"] = str(soup.find("h1",class_="align_left").string)

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
		return {"_id": listing_URL, "origin": origin}
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
	new_list = af_links(af_source)
	currentDB = collection.find({"origin":origin},{"_id":1})
	crawlList = copy.copy(new_list) ##going to crawl crawlList after it has been modified

	newCount = 0
	removeCount = 0

	current_DB = []
	for item in currentDB:
		current_DB.append(item)

	for each_link in new_list: # Remove Listings from new list to crawl that I already have in the DB
		if {"_id":each_link} in current_DB:
			crawlList.remove(each_link)

	for listing in currentDB: # Removes Listings from DB that are not currently listed on Chinook's Website
		if listing["_id"] in newList:
			pass
		else:
			removeCount = removeCount + 1
			collection.remove(listing)

	# af_crawl(listing_URL, origin, special, contact):
	for link in crawlList:
		try:
			INSERTME = af_crawl(link, origin, special, contact)
			collection.insert(INSERTME)
			newCount = newCount + 1
		except pymongo.errors.DuplicateKeyError:
			pass

	print str(newCount) + " added to database for " + origin
	print str(removeCount) + " removed from database for " + origin

