from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def mallard_pm():
	DB_collection = collection
	source = 'https://mallardproperties.appfolio.com/listings/'
	origin = "mallardPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Mallard Properties",
			"address" : "1953 Garden Ave, Eugene, OR 97403",
			"phone" : "(541) 465-3825",
			"fax" : "(541) 485-8177",
			"email" : "info@mallardproperties.net",
			"hours" : "Monday - Friday 9am - 5pm"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)