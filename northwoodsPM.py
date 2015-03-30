from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def northwoods_pm():
	DB_collection = collection
	source = 'https://northwoods.appfolio.com/listings/'
	origin = "northwoodsPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Northwoods Property Management",
			"address" : "81 Centennial Loop #8, Eugene, OR 97401",
			"phone" : "(541) 914-2282",
			"fax" : "(866) 664-2150",
			"email" : "office@northwoodspm.com",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)

