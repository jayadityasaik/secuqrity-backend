from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)

database = client["secuqrity_database"]

users_collection = database["users"]

authenticators_collection = database["authenticators"]

authentication_logs_collection = database["authentication_logs"]