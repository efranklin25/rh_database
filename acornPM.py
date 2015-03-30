from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def acorn_pm():
	DB_collection = collection
	source = 'https://acornpm.appfolio.com/listings/'
	origin = "acornPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Acorn Property Management",
			"address" : "214 Pioneer Parkway West, Springfield, OR 97477",
			"phone" : "(541) 683-6166",
			"fax" : "(541) 683-1616",
			"email" : "info@acornpm.net",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)

