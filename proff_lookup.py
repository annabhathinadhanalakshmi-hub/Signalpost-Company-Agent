import requests


WIKIDATA_SPARQL_URL = (
    "https://query.wikidata.org/sparql"
)


def get_proff_company(company_number):
    """
    Look up a company in Wikidata using the
    Norwegian organisation number property (P2333).

    The function name is kept as get_proff_company
    so the existing app.py does not need to change yet.
    """

    query = f"""
    SELECT ?company ?companyLabel ?description WHERE {{
        ?company wdt:P2333 "{company_number}".
        
        SERVICE wikibase:label {{
            bd:serviceParam
                wikibase:language "en".
        }}
        
        OPTIONAL {{
            ?company schema:description ?description.
            FILTER(LANG(?description) = "en")
        }}
    }}
    LIMIT 1
    """

    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": (
            "SignalPost-Company-Agent/1.0 "
            "(educational project)"
        )
    }

    try:

        response = requests.get(
            WIKIDATA_SPARQL_URL,
            params={
                "query": query,
                "format": "json"
            },
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as error:

        print(
            "\nWikidata lookup failed:"
        )

        print(error)

        return None

    except ValueError:

        print(
            "\nWikidata returned invalid JSON."
        )

        return None

    bindings = (
        data
        .get("results", {})
        .get("bindings", [])
    )

    if not bindings:

        return None

    result = bindings[0]

    company_url = (
        result
        .get("company", {})
        .get("value")
    )

    company_name = (
        result
        .get("companyLabel", {})
        .get("value", "")
    )

    description = (
        result
        .get("description", {})
        .get("value", "")
    )

    if not company_url:

        return None

    entity_id = (
        company_url
        .rstrip("/")
        .split("/")
        [-1]
    )

    return {
        "company_number": company_number,

        "company_name":
            company_name,

        "description":
            description,

        "entity_id":
            entity_id,

        "source":
            "Wikidata",

        "source_url":
            company_url
    }


def display_proff_source(company):

    if company is None:

        print(
            "\nNo second-source evidence found."
        )

        return

    print("\n")
    print("=" * 70)
    print("                 SECOND SOURCE: WIKIDATA")
    print("=" * 70)

    print(
        f"\nCompany Number     : "
        f"{company.get('company_number', 'Not available')}"
    )

    print(
        f"Company Name       : "
        f"{company.get('company_name', 'Not available')}"
    )

    print(
        f"Description        : "
        f"{company.get('description', 'Not available')}"
    )

    print(
        f"Wikidata Entity    : "
        f"{company.get('entity_id', 'Not available')}"
    )

    print(
        f"Source             : "
        f"{company.get('source', 'Wikidata')}"
    )

    print(
        f"Source URL         : "
        f"{company.get('source_url', 'Not available')}"
    )

    print(
        "\nSecond-source evidence found."
    )

    print("\n" + "=" * 70)
    import requests


WIKIDATA_SPARQL_URL = (
    "https://query.wikidata.org/sparql"
)


def get_proff_company(company_number):
    """
    Retrieve company evidence from Wikidata
    using the Norwegian organisation number.
    """

    query = f"""
    SELECT
        ?company
        ?companyLabel
        ?description
        ?website
        ?countryLabel
        ?industryLabel
    WHERE {{

        ?company wdt:P2333 "{company_number}".

        OPTIONAL {{
            ?company wdt:P856 ?website.
        }}

        OPTIONAL {{
            ?company wdt:P17 ?country.
        }}

        OPTIONAL {{
            ?company wdt:P452 ?industry.
        }}

        OPTIONAL {{
            ?company schema:description ?description.
            FILTER(
                LANG(?description) = "en"
            )
        }}

        SERVICE wikibase:label {{
            bd:serviceParam
                wikibase:language "en".
        }}
    }}

    LIMIT 1
    """

    headers = {
        "Accept": (
            "application/sparql-results+json"
        ),
        "User-Agent": (
            "SignalPost-Company-Agent/1.0 "
            "(educational project)"
        )
    }

    try:

        response = requests.get(
            WIKIDATA_SPARQL_URL,
            params={
                "query": query,
                "format": "json"
            },
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as error:

        print(
            "\nWikidata lookup failed:"
        )

        print(error)

        return None

    except ValueError:

        print(
            "\nWikidata returned invalid JSON."
        )

        return None

    bindings = (
        data
        .get("results", {})
        .get("bindings", [])
    )

    if not bindings:

        return None

    result = bindings[0]

    company_url = (
        result
        .get("company", {})
        .get("value", "")
    )

    if not company_url:

        return None

    entity_id = (
        company_url
        .rstrip("/")
        .split("/")
        [-1]
    )

    company_name = (
        result
        .get("companyLabel", {})
        .get("value", "")
    )

    description = (
        result
        .get("description", {})
        .get("value", "")
    )

    website = (
        result
        .get("website", {})
        .get("value", "")
    )

    country = (
        result
        .get("countryLabel", {})
        .get("value", "")
    )

    industry = (
        result
        .get("industryLabel", {})
        .get("value", "")
    )

    return {
        "company_number":
            company_number,

        "company_name":
            company_name,

        "description":
            description,

        "website":
            website,

        "country":
            country,

        "industry_description":
            industry,

        "entity_id":
            entity_id,

        "source":
            "Wikidata",

        "source_url":
            company_url
    }


def display_proff_source(company):

    if company is None:

        print(
            "\nNo second-source evidence found."
        )

        return

    print("\n")
    print("=" * 70)
    print("                 SECOND SOURCE: WIKIDATA")
    print("=" * 70)

    print(
        f"\nCompany Name       : "
        f"{company.get('company_name', 'Not available')}"
    )

    print(
        f"Company Number     : "
        f"{company.get('company_number', 'Not available')}"
    )

    print(
        f"Description        : "
        f"{company.get('description', 'Not available')}"
    )

    print(
        f"Website            : "
        f"{company.get('website', 'Not available')}"
    )

    print(
        f"Country            : "
        f"{company.get('country', 'Not available')}"
    )

    print(
        f"Industry           : "
        f"{company.get('industry_description', 'Not available')}"
    )

    print(
        f"Wikidata Entity    : "
        f"{company.get('entity_id', 'Not available')}"
    )

    print(
        f"Source             : "
        f"{company.get('source', 'Wikidata')}"
    )

    print(
        f"Source URL         : "
        f"{company.get('source_url', 'Not available')}"
    )

    print(
        "\nSecond-source evidence found."
    )

    print("\n" + "=" * 70)