import requests


API_BASE = "https://data.brreg.no/enhetsregisteret/api/enheter"


def get_company(company_number):
    url = f"{API_BASE}/{company_number}"

    response = requests.get(url, timeout=20)

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()