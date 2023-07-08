import pymongo
import CONSTANTS

def make_connection(collection_name):
    my_client = pymongo.MongoClient(CONSTANTS.MONGO_URL)
    my_db = my_client[CONSTANTS.DB_NAME]
    return my_db[collection_name]