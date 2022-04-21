
from services.company_service import CompanyService

company_service = CompanyService()

def query_all():
    # 1. Query the bad companies
    company_service.query_bad_companies()
    # 2. Query companies score < 50
    company_service.query_companies_by_lt_score(50)
    # print(companies)


if __name__ == "__main__":
    query_all()