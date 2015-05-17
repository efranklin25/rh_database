from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def valleyinvestment_pm():
	DB_collection = collection
	source = 'https://valleyinvestmentprop.appfolio.com/listings/'
	origin = "valleyinvestmentPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Valley Investment Properties",
			"address" : "1388 Willamette Street, Eugene, OR 97401",
			"phone" : "(541) 345-1641",
			"fax" : "(541) 345-1537",
			"email" : "N/A",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)



