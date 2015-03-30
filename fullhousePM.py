from appfolio_tools import af_update_crawl
from serverConfig import collection
import pymongo

def full_house_pm():
	DB_collection = collection
	source = 'https://fullhouserentals.appfolio.com/listings/'
	origin = "fullHousePM"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Full House Property Managerment, LLC",
			"address" : "1660 River Road, Eugene, OR 97404",
			"phone" : "(541) 357-7138",
			"fax" : "(866) 575-7410",
			"email" : "rentals@FullHouseRentals.com",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}

	af_update_crawl(DB_collection, source, origin, special, contact)