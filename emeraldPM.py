from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def emerald_pm():
	DB_collection = collection
	source = 'https://emerald.appfolio.com/listings/'
	origin = "emeraldPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Emerald Property Management",
			"address" : "525 Harlow Road, Springfield, OR 97477",
			"phone" : "(541) 741-4676",
			"fax" : "(541) 744-2849",
			"email" : "contactus@emeraldpm.com",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)