from services.db import company_collection 
from util.logger import logger
import requests
import traceback
from configuration.config import get_configuration

config = get_configuration()
token = config["tianyancha"]["token"]
base_info_url = "https://open.api.tianyancha.com/services/open/ic/baseinfo/normal"
search_url = "https://open.api.tianyancha.com/services/open/search/2.0"
headers = {
    "Authorization" : token
}

class TianYanCha:
    def __init__(self, ):
        pass

    def enrich_companies(self,):
        # get data from db:
        query = {"tianyancha.found": False, "tianyancha.searched": False}
        all_companies = company_collection.find(query)
        for company in all_companies:
            # print(company["name"])
            self.enrich_one_company(company)
    def process_company_name(self, name):
        # rule 1: remove the text from the last "（". for example, "德仪洋行企业发展（上海）有限公司（德仪洋行）" should be "德仪洋行企业发展（上海）"
        # rule 2: if the ) displays at last, remove it. for example 海焱起餐饮管理有限公司  (品牌名称：关东小磨) should be 海焱起餐饮管理有限公司
        rfind = name.rfind("（") 
        rfind_right = name.rfind("）") 
        find = name.find("（")
        company_name = name
        if rfind != -1 and rfind != find:
            company_name = company_name[0:rfind]
        if rfind_right == len(company_name) - 1: 
            # ) is the last character. remove the content of ()
            company_name = company_name[0:find]
        # english ()
        rfind_en = name.rfind("(") 
        rfind_en_right = name.rfind(")")
        find_en = name.find("(")
        if rfind_en != -1 and rfind_en != find_en:
            company_name = company_name[0:rfind_en]
        if rfind_en_right == len(company_name) - 1: 
            # ) is the last character. remove the content of ()
            company_name = company_name[0:find_en]

        return company_name
    def enrich_one_company(self, company):
        # query the tianyancha api to get the company info
        company_name = self.process_company_name(company["name"])
        data = self.query_company(company_name)
        tianyancha = {}
        if data == None:
            # Nothing found for this company, use the search function to enrich it
            company_id = self.search_company(company_name)
            if company_id == None:
                # not found or search failed
                tianyancha["found"] = False
                tianyancha["data"] = {}
                tianyancha["searched"] = True
            else:
                data = self.query_company(company_id)
                if data == None:
                    tianyancha["found"] = False
                    tianyancha["data"] = {}
                    tianyancha["searched"] = True
                else: 
                    tianyancha["found"] = True
                    tianyancha["data"] = data
                    tianyancha["searched"] = False
        else: 
            # data found
            tianyancha["found"] = True
            tianyancha["data"] = data
            tianyancha["searched"] = False
        self.update_db(company["id"], tianyancha)
        
    def update_db(self, company_id, tianyancha):
        #only update the tinayancha field
        # logger.info(f"Updating data for company_id: {company_id}")
        company_collection.update_one({"id": company_id}, {"$set":{"tianyancha": tianyancha}})
    
    def search_company(self, company_name):
        logger.info(f"Searching tianyancha for company {company_name}")
        try:
            res = requests.get(search_url + "?word=" + company_name, headers=headers)
            search_data = res.json()
            if search_data["error_code"] == 0:
                # company found
                # logger.info(f"Company found: {company_name}")
                if search_data["result"]["total"] == 0:
                    logger.info(f"0 Search result for company: {company_name}")
                    return None
                search_items = search_data["result"]["items"]
                # always return the first search result id.
                return search_items[0]["id"]
            else:
                logger.info(f"Search failed for company: {company_name}")
                return None
        except Exception as e:
            logger.error(repr(e))
            traceback.print_exc()
            logger.error(f"Error occurred during query_company({company_name})")
            return None

    def query_company(self, company_name):
        logger.info(f"Querying tianyancha for company {company_name}")
        try:
            res = requests.get(base_info_url + "?keyword=" + str(company_name), headers=headers)
            company_info = res.json()
            if company_info["error_code"] == 0:
                # company found
                # logger.info(f"Company found: {company_name}")
                return company_info["result"]
            else:
                logger.info(f"Company not found: {company_name}")
                return None
        except Exception as e:
            logger.error(repr(e))
            traceback.print_exc()
            logger.error(f"Error occurred during query_company({company_name})")
            return None


