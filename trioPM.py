from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def trio_pm():
	DB_collection = collection
	source = 'https://trio.appfolio.com/listings/'
	origin = "trioPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Trio Property Management Inc.",
			"address" : "1000 Willagillespie Road, Eugene, OR 97401",
			"phone" : "(541) 434-1900",
			"fax" : "(541) 434-1901",
			"email" : "info@triopm.com",
			"hours" : "Monday - Friday 9am - 5pm"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)