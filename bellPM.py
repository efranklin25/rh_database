from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def bell_pm():
	DB_collection = collection
	source = 'https://bell.appfolio.com/listings/?1426735307902&filters%5Bproperty_list%5D=Non%20Campus%20Properties'
	origin = "BellPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Bell Real Estate, Inc",
			"address" : "630 River Road, Eugene, OR 97404",
			"phone" : "(541) 688-2060",
			"fax" : "(541) 688-9728",
			"email" : "briank@bell-realty.com",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)

def bell_campus_pm():
	DB_collection = collection
	source = 'https://bell.appfolio.com/listings/?1426736434892&filters%5Bproperty_list%5D=CAMPUS%20PROPERTIES'
	origin = "Bell_CampusPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Bell Real Estate, Inc",
			"address" : "2001 Franklin Blvd., Eugene, OR 97403",
			"phone" : "(541) 687-1663",
			"fax" : "(541) 687-2327",
			"email" : "Campus@bell-realty.com",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)