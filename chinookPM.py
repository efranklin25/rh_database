from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def chinook_pm():
	DB_collection = collection
	source = 'https://chinookproperties.appfolio.com/listings/'
	origin = "ChinookPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Chinook Properties",
			"address" : "1590 High St. Eugene, OR 97401",
			"phone" : "(541) 484-0493",
			"fax" : "(541) 343-7507",
			"email" : "info@chinookproperties.net",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)
