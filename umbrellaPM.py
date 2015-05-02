import urllib2
from bs4 import BeautifulSoup
from listing_tools import get_type, get_location, is_student, is_pet_ok, lease_type
import pymongo
import json
from pprint import pprint



req_url = "http://umbrellaproperties.com/wordpress/wp-admin/admin-ajax.php"
req_data = "action=wpp_property_overview_pagination&%5Bpagination%5B=off&wpp_ajax_query%5Bquery%5D%5Bproperty_type%5D=floorplan&wpp_ajax_query%5Bthumbnail_size%5D=thumbnail"

def get_page_listings(url, form_data):
	req = urllib2.Request(url, form_data)
	response = urllib2.urlopen(req).read()
	doc = json.JSONDecoder().decode(response[response.index('{'):])
	current_list = []

	the_soup = BeautifulSoup(doc["display"])

	get_links = the_soup.find_all("a", rel="properties")

	for link in get_links:
		var = link.get('href')
		current_list.append(var)

	return current_list

current_listings = get_page_listings(req_url, req_data)

description_urls = set()

for url in current_listings:
	description_urls.add(url[:(url[:-2].rfind('/')+1)])

description_data = {}

for url in description_urls:
	key = url[url[:-2].rfind('/')+1:url.rfind('/')]
	soup = BeautifulSoup(urllib2.urlopen(url).read())
	value = ''
	count = 0
	for obj in soup.find_all('p', limit=3):
		count = count + 1
		if count == 3:
			if obj.string == None:
				pass
			else:
				value = value + unicode(obj.string)
		else:
			value = value + unicode(obj.string) + '<br>'
	description_data[key] = value



def crawl(listing_URL, origin, special, contact, desc_data):
	soup = BeautifulSoup(urllib2.urlopen(listing_URL).read())
	soupStrings = soup.find_all(text=True)

	base = listing_URL[:(listing_URL[:-2].rfind('/')+1)]
	key = base[base[:-2].rfind('/')+1:base.rfind('/')]

	spans = soup.find_all("span")
	strings = []
	petloc = -1

	for item in spans:
		try:
			if item["class"] == ["value"]:
				value = unicode(item.string)
				strings.append(value[:-1])
				if 'Pet' in value:
					petloc = strings.index(value[:-1])
		except KeyError:
			pass

	data = {
		'available' : strings[0],
		'address' : strings[1],
		'cost' : int(strings[3].replace('$','')), 
		'pet' : strings[petloc],
		'size' : int(strings[11]),
		'bed' : int(strings[4]),
		'bath' : int(strings[5])
	}


	jsonDoc = {}
	jsonDoc["URL"] = listing_URL
	jsonDoc["origin"] = origin
	jsonDoc["title"] = str(soup.find("h1",class_="property-title entry-title").string).strip()

	#get rental cost as integer, removing comma if present in value
	if data['cost'] == 0:
		return {"URL": listing_URL, "origin": origin}
	jsonDoc["cost"] = data['cost']

	# number of days between payments, 30 = monthly, 7 = weekly etc
	jsonDoc["costType"] = 30

	#get listing location
	jsonDoc["location"] = get_location(data['address'])


	jsonDoc["description"] = desc_data[key]

	jsonDoc["type"] = get_type(jsonDoc["description"])

	#get list of images in listing
	imageObject = soup.find_all("a", class_="highslide")
	imageList = []
	for link in imageObject:
		imageList.append(link.get('href'))
	if imageList == []:
		imageList.append("/static/house.png")
#	jsonDoc["images"] = imageList

#	jsonDoc["amenities"] = 

	#get square footage as an integer (0 = unspecified)
	jsonDoc["sizeSQF"] = data["size"]

	#get int for bedrooms and bathrooms * NOTE THIS WILL NOT WORK IF THERE ARE MORE THAN 9 BEDROOMS OR BATHROOMS
	jsonDoc["bedrooms"] = data["bed"]
	jsonDoc["bathrooms"] = data["bath"]

	#get available date as a string
	jsonDoc["available"] = data['available']

	#get application fee as an int
	jsonDoc["appFee"] = 35

	#get security deposit as an integer, must remove comma from value to create integer
	try:
		secDepLoc = soupStrings.index('Security Deposit:')
		secDep = soupStrings[secDepLoc+1].strip()
		securityDeposit = int(secDep[1:].replace(',',''))
	except ValueError:
		securityDeposit = 0
#	jsonDoc["secDeposit"] = securityDeposit

	jsonDoc["pets"] = is_pet_ok(data['pet'], data['pet'])

#	jsonDoc["lease"] = lease_type(jsonDoc["description"], jsonDoc["amenities"])

	#Does this listing accept Section 8, HACSA
#	jsonDoc["special"] = special

#	jsonDoc["student"] = is_student(jsonDoc["description"], jsonDoc["title"])

	jsonDoc["applyNow"] = "http://umbrellaproperties.com/apply-online/"

	jsonDoc["contact"] = contact

	return jsonDoc

def update_crawl(collection, origin, special, contact, new_list):
	currentDB = collection.find({"origin":origin},{"URL":1})
	crawlList = copy.copy(new_list) ##going to crawl crawlList after it has been modified

	newCount = 0
	removeCount = 0

	current_DB = []
	for item in currentDB:
		current_DB.append(item)

	for each_link in new_list: # Remove Listings from new list to crawl that I already have in the DB
		if {"URL":each_link} in current_DB:
			crawlList.delete_one(each_link)

	for listing in current_DB: # Removes Listings from DB that are not currently listed on Chinook's Website
		if listing["URL"] in new_list:
			pass
		else:
			removeCount = removeCount + 1
			collection.delete_one({"URL": listing["URL"]})

	# af_crawl(listing_URL, origin, special, contact):
	# May want to use insert_many() **new in mongo 3.0....
	for link in crawlList:
		try:
			INSERTME = crawl(link, origin, special, contact)
			collection.insert_one(INSERTME)
			newCount = newCount + 1
		except pymongo.errors.DuplicateKeyError:
			pass

	print str(newCount) + " added to database for " + origin
	print str(removeCount) + " removed from database for " + origin