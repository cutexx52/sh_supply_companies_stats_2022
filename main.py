from services.data_crawer import DataCrawer
from services.company_service import CompanyService
from services.tianyancha_service import TianYanCha
data_crawer = DataCrawer()
company_service = CompanyService()
tianyancha = TianYanCha()
def main():
    # 1. query the data from the website
    # all_companies = data_crawer.query_all()
    # 2. store the companies to DB
    # company_service.store_to_db(all_companies)
    # 3. call the 天眼查 api to add more information for each company
    tianyancha.enrich_companies()
    # 3.1 test: enrich one company
    # tianyancha.enrich_one_company({
    #     "id": 221,
    #     "name": "上海伊禾商贸有限公司"
    # })

if __name__ == "__main__":
    main()