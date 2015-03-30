from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def principle_pm():
	DB_collection = collection
	source = 'https://principle.appfolio.com/listings/'
	origin = "principlePM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Principle Property Management",
			"address" : "4710 Village Plaza Loop Suite 135, Eugene, OR 97401",
			"phone" : "(541) 345-6789",
			"fax" : "(541) 284-8111",
			"email" : "info@principlepm.com",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)

