import re
import logging
from zipcodes import zip_codes

#from listing_tools import get_type, is_pet_ok, lease_type, is_student, get_location

def get_type(description_string):
	listing_type = ''

	# 4 listing types, Condo, Apartment and Studio.  If not a Studio, Apartment or Condo, then it is a House.

	Condo = ['Condo', 'condo']
	Apartment = ['apartment', 'Apartment', 'apt', 'Apt']
	Studio = ['studio', 'Studio']

	for string in Studio:
		if string in description_string:
			listing_type = 'Studio'
			break

	if len(listing_type) > 1:
		return listing_type

	for string in Apartment:
		if string in description_string:
			listing_type = 'Apartment'
			break

	if len(listing_type) > 1:
		return listing_type

	for string in Condo:
		if string in description_string:
			listing_type = 'Condo'
			break

	listing_type = 'House'

	return listing_type

def is_pet_ok(description, amenity_list):
    #Returns dictionary of dogs and cats with values as integers, respresenting either: 0 = No, 1 = Yes, 2 = Unspecified("Contact for Information")
    no_pet = ['NO PET', 'NO PETS', 'NOT ACCEPT PETS', 'NOT ACCEPT PET', 'PETS ARE NOT', 'PET IS NOT']
    yes_dog = ['DOGS ALLOWED', 'DOG ALLOWED', 'DOGS ONLY', 'DOG ONLY', 'DOGS PERMITTED', 'DOG PERMITTED', '1 DOG', 'ONE DOG']
    yes_cat = ['CATS ALLOWED', 'CAT ALLOWED', 'CATS ONLY', 'CAT ONLY', 'CATS PERMITTED', 'CAT PERMITTED', '1 CAT', 'ONE CAT']
    yes_pet = ['PETS ALLOWED', 'PET ALLOWED', 'CATS AND DOGS ALLOWED', 'CATS & DOGS ALLOWED', 'PETS PERMITTED', 'PET PERMITTED']
    
    pets = {"dogs" : 2, "cats" : 2}

    for keyword in no_pet:
        if keyword in description.upper():
            pets['dogs'] = 0
            pets['cats'] = 0
            return pets
        else:
            for amenity in amenity_list:
                if keyword in amenity.upper():
                    pets['dogs'] = 0
                    pets['cats'] = 0
                    return pets

    for keyword in yes_pet:
        if keyword in description.upper():
            pets['dogs'] = 1
            pets['cats'] = 1
            break
        else:
            for amenity in amenity_list:
                if keyword in amenity.upper():
                    pets['dogs'] = 1
                    pets['cats'] = 1
                    break

    for keyword in yes_dog:
        if keyword in description.upper():
            pets['dogs'] = 1
            pets['cats'] = 0
            return pets
        else:
            for amenity in amenity_list:
                if keyword in amenity.upper():
                    pets['dogs'] = 1
                    pets['cats'] = 0
                    return pets

    for keyword in yes_cat:
        if keyword in description.upper():
            pets['cats'] = 1
            pets['dogs'] = 0
            return pets
        else:
            for amenity in amenity_list:
                if keyword in amenity.upper():
                    pets['cats'] = 1
                    pets['dogs'] = 0
                    return pets

    return pets


def lease_type(description, amenity_list):
	#Return integers, representing either: 0 = Unspecified("Contact for Information"), 1 = Month to Month, all other int = int x # of months ie. 12 = 12 Month, 6 = 6 Month
    m2m = ['MONTH TO MONTH', 'M2M']
    term_months = ['MONTH LEASE', 'MTH LEASE', 'MO LEASE', 'MO. LEASE']
    year_term = ['ONE YEAR LEASE', "1 YEAR LEASE", "1 YR LEASE", "ONE YR LEASE", 'LEASE IS 1 YEAR', 'LEASE IS ONE YEAR']
    two_year = ['TWO YEAR LEASE', "2 YEAR LEASE", "2 YR LEASE", "TWO YR LEASE", 'LEASE IS 2 YEAR', 'LEASE IS TWO YEAR']

    for keyword in m2m:
        if keyword in description.upper():
            return 1
        else:
            for amenity in amenity_list:
                if keyword in amenity.upper():
                    return 1

    for keyword in year_term:
        if keyword in description.upper():
            return 12
        else:
            for amenity in amenity_list:
                if keyword in amenity.upper():
                    return 12

    for keyword in two_year:
        if keyword in description.upper():
            return 24
        else:
            for amenity in amenity_list:
                if keyword in amenity.upper():
                    return 24

    for keyword in term_months:
        if keyword in description.upper():
            ref = description.upper().index(keyword) #Reference begining of "MONTH LEASE", ie. "6 MONTH LEASE"
            begining = description.upper().index(" ", 0, ref-2) #reference the 1st " " space after the number
            try:
                lease = int(description[begining:ref].strip()) #does it make an integer? if so this is your months
                return lease
            except ValueError:
                pass
        else:
            for amenity in amenity_list:
                if keyword in amenity_list:
                    ref = description.upper().index(keyword)
                    begining = description.upper().index(" ", 0, ref-2)
                    try:
                        lease = int(description[begining:ref].strip())
                        return lease
                    except ValueError:
                        pass

	return 0 #Unspecified 


def is_student(description, title):
	keywords = ['CAMPUS', 'STUDENT', 'STUDENTS', 'CLOSE TO UNIVERSITY', 'NEAR UNIVERSITY', 'MIN FROM UNIVERSITY', 'MINUTES FROM UNIVERSITY', 'MIN FROM CAMPUS', 'MINUTES FROM CAMPUS']
	false_keywords = ['NON STUDENT', 'NO STUDENT', 'NO STUDENTS', 'NON STUDENTS']

	for keyword in false_keywords:
		if keyword in description.upper():
			return False
		else:
			if keyword in title.upper():
				return False

	for keyword in keywords:
		if keyword in description.upper():
			return True
		else:
			if keyword in title.upper():
				return True
	return False 

def get_location(address_string):
    city = ''
    state = ''
    zip_code = ''
    county = ''
    state = ''

    address_digits = re.findall('\d+', address_string)

    if address_digits[-1] in zip_codes:
        zip_code = address_digits[-1]
        city = zip_codes[zip_code]["city"] 
        state = zip_codes[zip_code]["state"]
        county = zip_codes[zip_code]["county"]
        if city in address_string:
            address = address_string[:(address_string.index(city))].replace(',', '').strip()
        else:
            try:
                address = address_string[:address_string.index(',')]
            except ValueError:
                address = address_string[:address_string.index(zip_code)]
    else:
        address = address_string

    location = {
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "county": county,
        "address": address,
    }

    return location

