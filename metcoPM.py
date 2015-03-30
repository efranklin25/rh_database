from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def metco_pm():
	DB_collection = collection
	source = 'https://metco.appfolio.com/listings/'
	origin = "metcoPM"
	special = {"section8" : True, "hacsa" : False}
	contact = {
			"name" : "METCO Investment Reality, Inc.",
			"address" : "1810 15th Street, Springfield, OR 97477",
			"phone" : "(541) 683-9001",
			"fax" : "(541) 683-3957",
			"email" : "No E-Mail",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)