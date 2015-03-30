from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def jennings_group_pm():
	DB_collection = collection
	source = 'https://jenningsgroup.appfolio.com/listings/'
	origin = "jenningsGroupPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Jennings Group, Incorporated",
			"address" : "488 East 11th Ave, Eugene, OR 97401",
			"phone" : "(541) 683-2271",
			"fax" : "(541) 683-5983",
			"email" : "No E-Mail",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)