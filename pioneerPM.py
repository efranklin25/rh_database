from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def pioneer_pm():
	DB_collection = collection
	source = 'https://pioneer.appfolio.com/listings/'
	origin = "pioneerPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Pioneer Property Management",
			"address" : "4725 Village Plaza Loop, Suite 200, Eugene, OR 97401",
			"phone" : "(541) 687-9090",
			"fax" : "No Fax",
			"email" : "No E-Mail",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)