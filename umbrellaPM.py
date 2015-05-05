import urllib2
from bs4 import BeautifulSoup
from listing_tools import get_type, get_location, is_student, is_pet_ok, lease_type
import pymongo
import json
from serverConfig import collection
import copy
import sys

def umbrella_pm():

	req_url = "http://umbrellaproperties.com/wordpress/wp-admin/admin-ajax.php"
	req_data = "action=wpp_property_overview_pagination&%5Bpagination%5B=off&wpp_ajax_query%5Bquery%5D%5Bproperty_type%5D=floorplan&wpp_ajax_query%5Bthumbnail_size%5D=thumbnail"

	origin = "umbrellaPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Umbrella Property Managerment",
			"address" : "91120 N. Willamette, Coburg, OR 97408",
			"phone" : "(541) 484-6595",
			"fax" : "(541) 484-4395",
			"email" : "N/A",
			"hours" : "Monday-Friday 8:30 AM - 5PM"
		}

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

	current_list = get_page_listings(req_url, req_data) #list of listing urls that are currently posted on the PM's website
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

	description_urls = set()

	for url in crawl_list:
		description_urls.add(url[:(url[:-2].rfind('/')+1)])

	description_data = {}

	for url in description_urls:
		key = url[url[:-2].rfind('/')+1:url.rfind('/')]
		soup = BeautifulSoup(urllib2.urlopen(url).read())
		value = ''
		count = 0
		amenities = []

		try:
			div = soup.find('div', class_="property_feature_list")
			for obj in div.find_all('li'):
				amenities.append(unicode(obj.string))
			for obj in soup.find_all('p', limit=3):
				count = count + 1
				if count == 3:
					if obj.string == None:
						pass
					else:
						value = value + unicode(obj.string)
				else:
					value = value + unicode(obj.string) + '<br>'
		except AttributeError:
			amenities = []
			value = ''

		description_data[key] = {'description' : value, 'amenities': amenities}




	def crawl(listing_URL, origin, special, contact, desc_data):
		try:
			soup = BeautifulSoup(urllib2.urlopen(listing_URL).read())
			soupStrings = soup.find_all(text=True)

			base = listing_URL[:(listing_URL[:-2].rfind('/')+1)]
			key = base[base[:-2].rfind('/')+1:base.rfind('/')]

			property_stats = soup.find('ul', id="property_stats")	

			jsonDoc = {}
			jsonDoc["URL"] = listing_URL
			jsonDoc["origin"] = origin
			jsonDoc["title"] = str(soup.find("h1",class_="property-title entry-title").string).strip()

			#get rental cost as integer, removing comma if present in value
			price = unicode(property_stats.find('li', class_="property_price").find('span', class_="value").string.strip().replace("$", ""))
			if price == None:
				return {"URL": listing_URL, "origin": origin}
			jsonDoc["cost"] = int(price)

			# number of days between payments, 30 = monthly, 7 = weekly etc
			jsonDoc["costType"] = 30

			#get listing location
			jsonDoc["location"] = get_location(unicode(property_stats.find('li', class_="wpp_stat_plain_list_location").find('span', class_="value").string.strip()))


			jsonDoc["description"] = description_data[key]['description']

			jsonDoc["type"] = get_type(jsonDoc["description"])

			#get list of images in listing
			imageList = []
			img_div = soup.find('div', class_="ngg-galleryoverview")
			for obj in img_div.find_all('a'):
				imageList.append(unicode(obj.get('href')))
			if imageList == []:
				imageList.append("/static/house.png")
			jsonDoc["images"] = imageList
		 

			jsonDoc["amenities"] = description_data[key]['amenities']

			#get square footage as an integer (0 = unspecified)
			size_string = unicode(property_stats.find('li', class_="property_square_feet").find('span', class_="value").string.strip())
			try:
				the_size = int(size_string)
			except ValueError:
				the_size = 0
			jsonDoc["sizeSQF"] = the_size

			#get int for bedrooms and bathrooms
			bed_string = unicode(property_stats.find('li', class_="property_bedrooms").find('span', class_="value").string.strip())
			try:
				beds = int(bed_string)
			except ValueError:
				beds = 1
			jsonDoc["bedrooms"] = beds
			bath_string = unicode(property_stats.find('li', class_="property_bathrooms").find('span', class_="value").string.strip())
			try:
				baths = int(bath_string)
			except ValueError:
				baths = 1
			jsonDoc["bathrooms"] = baths

			#get available date as a string
			jsonDoc["available"] = unicode(property_stats.find('li', class_="wpp_stat_plain_list_date_open").find('span', class_="value").string.strip())

			#get application fee as an int
			jsonDoc["appFee"] = 35

			#get security deposit as an integer, 0 = Unspecified
			deposit_string = unicode(property_stats.find('li', class_="property_deposit").find('span', class_="value").string.strip())
			try:
				deposit = int(deposit_string)
			except ValueError:
				deposit = 0
			jsonDoc["secDeposit"] = 0

			pet_string = unicode(property_stats.find('li', class_="property_pet_policy").find('span', class_="value").string.strip())
			jsonDoc["pets"] = is_pet_ok(pet_string, pet_string)

			lease_string = unicode(property_stats.find('li', class_="property_lease_terms").find('span', class_="value").string.strip())
			jsonDoc["lease"] = lease_type(jsonDoc["description"], lease_string)

			#Does this listing accept Section 8, HACSA
			jsonDoc["special"] = special

			jsonDoc["student"] = is_student(jsonDoc["description"], jsonDoc["title"])

			jsonDoc["applyNow"] = "http://umbrellaproperties.com/apply-online/"

			jsonDoc["contact"] = contact

			return jsonDoc
		except:
			print listing_URL
			raise

	# crawl(listing_URL, origin, special, contact, desc_data)
	# May want to use insert_many() **new in mongo 3.0....
	for link in crawl_list:
		try:
			INSERTME = crawl(link, origin, special, contact, description_data) 
			collection.insert_one(INSERTME)
			newCount = newCount + 1
		except:
			print link + "did not work because..."
			print sys.exc_info()
			pass

	print str(newCount) + " added to database for " + origin
	print str(removeCount) + " removed from database for " + origin








