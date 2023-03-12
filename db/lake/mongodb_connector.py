from pymongo import MongoClient

def connect_to_mongodb():
    return MongoClient('localhost', 27017)