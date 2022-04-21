
from services.company_service import CompanyService

company_service = CompanyService()

def query_all():
    # 1. Query the bad companies
    company_service.query_bad_companies()
    # print(companies)


if __name__ == "__main__":
    query_all()