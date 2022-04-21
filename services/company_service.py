# DB operations about a company
import json
from configuration.config import get_configuration
from util.logger import logger
from services.db import company_collection
from mongodb_scripts.bad_company_aggr import pipelines
import csv

config = get_configuration()


class CompanyService:
    def __init__(self):
        pass
    def store_to_db(self, data):
        if len(data) == 0:
            logger.info("No item in data")
        company_collection.insert_many(data)
    def query_bad_companies(self):
        to_csv = list(company_collection.aggregate(pipelines))
        keys = to_csv[0].keys()
        with open('outputs/bad_companies.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(to_csv)
    def query_companies_by_lt_score(self, score):
        to_csv = company_collection.find({"tianyancha.data.percentileScore": {"$lt": score * 100}}, {"name": 1})
        keys = to_csv[0].keys()
        with open(f"outputs/lt_{score}_companies.csv", 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(to_csv)
