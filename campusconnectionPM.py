from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def campusconnection_pm():
	DB_collection = collection
	source = 'https://campusconnection.appfolio.com/listings/'
	origin = "campusconnectionPM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Campus Connection Property Management, LLC",
			"address" : "236 East 13th Unit 1, Eugene, OR 97401",
			"phone" : "(541) 556-1144",
			"fax" : "(541) 344-1522",
			"email" : "info@oregoncampusrentals.com",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)