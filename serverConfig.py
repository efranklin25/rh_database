import pymongo

connection = pymongo.Connection("mongodb://localhost", safe=True)
db = connection.project
collection = db.listings#This is the DB/Server Confirguration file for all myHome Classes

