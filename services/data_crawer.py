
from configuration.config import get_configuration
import requests, json
import traceback
from util.logger import logger

config=get_configuration()
class DataCrawer:
    def __init__(self):
        self.api_link = "https://c.kdcer.com/sh_keep_supply/home/enterprises?categoryId=-1&keyword=&limit=20"

    def query_once(self, page_num):
        # call the api once and return the data
        try:    
            data = requests.get(self.api_link + "&page=" + str(page_num),)
            data = data.json()
            return data["data"]
        except Exception as e:
            logger.error(repr(e))
            traceback.print_exc()
            logger.error('Error occurred during query_once({})'.format(page_num))
    
    def query_all(self):
        # call the api until the returned data is empty
        call_finished = False
        result = []
        current_page = 1
        while not call_finished:
            data = self.query_once(current_page)
            if len(data) == 0:
                call_finished = True
            else:
                result.extend(data)
                current_page += 1
        return result


    