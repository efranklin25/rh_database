import pymongo

#The client object is thread-safe and has connection-pooling built in. If an operation fails because of a network error, ConnectionFailure is raised 
#and the client reconnects in the background. Application code should handle this exception (recognizing that the operation failed) and then continue to execute.

connection = pymongo.MongoClient('localhost', 27017)
db = connection.project
collection = db.listings#This is the DB/Server Confirguration file for all myHome Classes

