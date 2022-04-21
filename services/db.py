import pymongo
from configuration.config import get_configuration
config = get_configuration()
client = pymongo.MongoClient(config["mongodb"]["uri"])
db = client["company"]
company_collection = db["company"]
__all__ = ("db", "company_collection")