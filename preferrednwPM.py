from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def preferred_nw_pm():
	DB_collection = collection
	source = 'https://preferrednorthwestpm.appfolio.com/listings/'
	origin = "preferrednwPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Preferred Northwest Property Management",
			"address" : "100 Easat 11th Ave Suite C, Eugene, OR 97401",
			"phone" : "(541) 747-7243",
			"fax" : "(541) 505-8525",
			"email" : "info@preferrednorthwestpm.com",
			"hours" : "Monday - Friday 9am - 5pm"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)