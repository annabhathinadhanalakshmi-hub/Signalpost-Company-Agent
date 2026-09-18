import csv
from datetime import datetime, timezone

import requests


API_URL = "https://data.brreg.no/enhetsregisteret/api/enheter"

OUTPUT_FILE = "data/company_profiles.csv"


def get_profiles():

    params = {
        "organisasjonsform": "AS,ASA",
        "size": 1000,
        "page": 0,
        "sort": "organisasjonsnummer,ASC"
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data.get("_embedded", {}).get("enheter", [])


def clean_profile(company):

    organisation_type = company.get(
        "organisasjonsform"
    ) or {}

    address = company.get(
        "forretningsadresse"
    ) or {}

    industry = company.get(
        "naeringskode1"
    ) or {}

    address_lines = address.get(
        "adresse"
    ) or []

    company_number = company.get(
        "organisasjonsnummer"
    )

    return {
        "company_number": company_number,

        "company_name": company.get(
            "navn"
        ),

        "organisation_type": organisation_type.get(
            "beskrivelse"
        ),

        "organisation_code": organisation_type.get(
            "kode"
        ),

        "registration_date": company.get(
            "registreringsdatoEnhetsregisteret"
        ),

        "foundation_date": company.get(
            "stiftelsesdato"
        ),

        "industry_code": industry.get(
            "kode"
        ),

        "industry_description": industry.get(
            "beskrivelse"
        ),

        "employees": company.get(
            "antallAnsatte"
        ),

        "website": company.get(
            "hjemmeside"
        ),

        "email": company.get(
            "epostadresse"
        ),

        "phone": company.get(
            "telefon"
        ),

        "street": ", ".join(address_lines),

        "postal_code": address.get(
            "postnummer"
        ),

        "city": address.get(
            "poststed"
        ),

        "municipality": address.get(
            "kommune"
        ),

        "country": address.get(
            "land"
        ),

        "country_code": address.get(
            "landkode"
        ),

        "bankrupt": company.get(
            "konkurs"
        ),

        "under_liquidation": company.get(
            "underAvvikling"
        ),

        "source": "Brønnøysundregistrene",

        "source_url": (
            f"{API_URL}/{company_number}"
        ),

        "evidence_company_number": company_number,

        "retrieved_at": datetime.now(
            timezone.utc
        ).isoformat()
    }


def save_profiles(profiles):

    fieldnames = [
        "company_number",
        "company_name",
        "organisation_type",
        "organisation_code",
        "registration_date",
        "foundation_date",
        "industry_code",
        "industry_description",
        "employees",
        "website",
        "email",
        "phone",
        "street",
        "postal_code",
        "city",
        "municipality",
        "country",
        "country_code",
        "bankrupt",
        "under_liquidation",
        "source",
        "source_url",
        "evidence_company_number",
        "retrieved_at"
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(profiles)


def main():

    print("Fetching company profiles...")

    companies = get_profiles()

    print(
        f"Received {len(companies)} company profiles."
    )

    profiles = [
        clean_profile(company)
        for company in companies
    ]

    save_profiles(profiles)

    print(
        f"Saved {len(profiles)} profiles to:"
    )

    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()