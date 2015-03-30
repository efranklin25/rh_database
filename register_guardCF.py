from listing_tools import get_type, is_pet_ok, lease_type, is_student, get_location
from serverConfig import collection
import pymongo

def register_guard_cf():
	soup = 






	source = "http://housing.registerguard.com/homes/search/results?radius=0&view=List_Detail&sort=IsFeatured+desc%2C+MinPrice+desc&rows=1000&terms=for-rent"
	origin = "registerguardCF"
	special = {"section8" : False, "hacsa" : False}
	contact = {
			"name" : "Northwoods Property Management",
			"address" : "81 Centennial Loop #8, Eugene, OR 97401",
			"phone" : "(541) 914-2282",
			"fax" : "(866) 664-2150",
			"email" : "office@northwoodspm.com",
			"hours" : "Monday-Friday 9 AM - 5PM"
		}