from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def premier_pm():
	DB_collection = collection
	source = 'https://premierppm.appfolio.com/listings/'
	origin = "premierPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Premier Property Management",
			"address" : "697 Country Club Road, Eugene, OR 97401",
			"phone" : "(541) 343-2183",
			"fax" : "(541) 485-5024",
			"email" : "info@premierpropertymanagementservices.net",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)

