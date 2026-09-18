import csv
import sys
from datetime import datetime, timezone

from agent.company_lookup import get_company
from agent.proff_lookup import get_proff_company, display_proff_source
from agent.evidence_matcher import (
    match_company_evidence,
    display_evidence_report
)
from agent.risk_analyzer import (
    analyze_company_risk,
    display_risk_report
)


DATA_FILE = "data/company_profiles.csv"
DEMO_COMPANY_NUMBER = "923609016"


def find_local_company(company_number):
    """Search the saved company dataset."""

    try:
        with open(
            DATA_FILE,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                if row.get("company_number") == company_number:
                    return row

    except FileNotFoundError:
        return None

    return None


def convert_boolean(value):
    """Convert CSV boolean values into real Python booleans."""

    if value is None:
        return None

    value = str(value).strip().lower()

    if value == "true":
        return True

    if value == "false":
        return False

    return None


def convert_saved_company(company):
    """Convert a saved CSV profile into the internal format."""

    return {
        "company_number": company.get("company_number"),
        "company_name": company.get("company_name"),

        "organisation_type": company.get(
            "organisation_type"
        ),

        "registration_date": company.get(
            "registration_date"
        ),

        "foundation_date": company.get(
            "foundation_date"
        ),

        "industry_code": company.get(
            "industry_code"
        ),

        "industry_description": company.get(
            "industry_description"
        ),

        "employees": company.get("employees"),

        "website": company.get("website"),
        "email": company.get("email"),
        "phone": company.get("phone"),

        "street": company.get("street"),
        "postal_code": company.get("postal_code"),
        "city": company.get("city"),
        "municipality": company.get("municipality"),
        "country": company.get("country"),

        "bankrupt": convert_boolean(
            company.get("bankrupt")
        ),

        "under_liquidation": convert_boolean(
            company.get("under_liquidation")
        ),

        "source": company.get(
            "source",
            "Brønnøysundregistrene"
        ),

        "source_url": company.get(
            "source_url"
        ),

        "evidence_company_number": company.get(
            "evidence_company_number",
            company.get("company_number")
        ),

        "retrieved_at": company.get(
            "retrieved_at"
        ),

        "data_status": "Saved profile - API unavailable"
    }


def convert_api_company(company):
    """Convert Brønnøysundregistrene API data."""

    address = company.get(
        "forretningsadresse",
        {}
    )

    street_parts = address.get(
        "adresse",
        []
    )

    if isinstance(street_parts, list):
        street = ", ".join(street_parts)
    else:
        street = street_parts

    company_number = company.get(
        "organisasjonsnummer"
    )

    retrieved_at = datetime.now(
        timezone.utc
    ).isoformat()

    return {
        "company_number": company_number,

        "company_name": company.get(
            "navn"
        ),

        "organisation_type": (
            company.get(
                "organisasjonsform",
                {}
            ).get(
                "beskrivelse"
            )
        ),

        "registration_date": company.get(
            "registreringsdatoEnhetsregisteret"
        ),

        "foundation_date": company.get(
            "stiftelsesdato"
        ),

        "industry_code": (
            company.get(
                "naeringskode1",
                {}
            ).get(
                "kode"
            )
        ),

        "industry_description": (
            company.get(
                "naeringskode1",
                {}
            ).get(
                "beskrivelse"
            )
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

        "street": street,

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

        "bankrupt": company.get(
            "konkurs"
        ),

        "under_liquidation": company.get(
            "underAvvikling"
        ),

        "source": "Brønnøysundregistrene",

        "source_url": (
            "https://data.brreg.no/"
            "enhetsregisteret/api/enheter/"
            f"{company_number}"
        ),

        "evidence_company_number": company_number,

        "retrieved_at": retrieved_at,

        "data_status": "Fresh API lookup"
    }


def print_header():
    print("\n")
    print("=" * 72)
    print("                     SIGNALPOST")
    print("              COMPANY VERIFICATION AGENT")
    print("=" * 72)
    print(
        "  Multi-source company intelligence "
        "and evidence verification"
    )
    print("=" * 72)


def print_step(number, title):
    print("\n")
    print("-" * 72)
    print(f"  [{number}] {title}")
    print("-" * 72)


def print_company_summary(company):
    print("\n")
    print("  COMPANY SUMMARY")
    print("  " + "-" * 66)

    print(
        f"  Name           : "
        f"{company.get('company_name')}"
    )

    print(
        f"  Company Number : "
        f"{company.get('company_number')}"
    )

    print(
        f"  Organisation   : "
        f"{company.get('organisation_type')}"
    )

    print(
        f"  Industry       : "
        f"{company.get('industry_description')}"
    )

    print(
        f"  Location       : "
        f"{company.get('city')}, "
        f"{company.get('country')}"
    )

    print(
        f"  Employees      : "
        f"{company.get('employees')}"
    )

    print(
        f"  Website        : "
        f"{company.get('website')}"
    )

    print(
        f"  Data Status    : "
        f"{company.get('data_status')}"
    )

    print(
        f"  Retrieved At   : "
        f"{company.get('retrieved_at')}"
    )


def display_company_status(company):
    print("\n")
    print("  OFFICIAL STATUS")
    print("  " + "-" * 66)

    bankrupt = company.get(
        "bankrupt"
    )

    liquidation = company.get(
        "under_liquidation"
    )

    if bankrupt is True:
        print("  Bankruptcy      : YES")

    elif bankrupt is False:
        print("  Bankruptcy      : NO")

    else:
        print("  Bankruptcy      : NOT AVAILABLE")

    if liquidation is True:
        print("  Liquidation     : YES")

    elif liquidation is False:
        print("  Liquidation     : NO")

    else:
        print("  Liquidation     : NOT AVAILABLE")


def display_final_summary(
    company,
    second_source,
    evidence_report,
    risk_report
):
    print("\n")
    print("=" * 72)
    print("                  FINAL SIGNALPOST REPORT")
    print("=" * 72)

    print("\n  COMPANY")
    print("  " + "-" * 66)

    print(
        f"  {company.get('company_name')} "
        f"({company.get('company_number')})"
    )

    print("\n  DATA FRESHNESS")
    print("  " + "-" * 66)

    print(
        f"  Data Status      : "
        f"{company.get('data_status')}"
    )

    print(
        f"  Retrieved At     : "
        f"{company.get('retrieved_at')}"
    )

    print("\n  SOURCES")
    print("  " + "-" * 66)

    print(
        f"  Primary Source   : "
        f"{company.get('source')}"
    )

    print(
        f"  Primary URL      : "
        f"{company.get('source_url')}"
    )

    if second_source:

        print(
            f"  Second Source    : "
            f"{second_source.get('source', 'Wikidata')}"
        )

        print(
            f"  Second URL       : "
            f"{second_source.get('source_url')}"
        )

    else:

        print(
            "  Second Source    : "
            "NOT AVAILABLE"
        )

    print("\n  EVIDENCE")
    print("  " + "-" * 66)

    if evidence_report:

        print(
            f"  Verification     : "
            f"{evidence_report['verification_status']}"
        )

        print(
            f"  Evidence Coverage: "
            f"{evidence_report['coverage']}%"
        )

        print(
            f"  Available Match  : "
            f"{evidence_report['match_rate']}%"
        )

        print(
            f"  Matched Fields   : "
            f"{evidence_report['matched_fields']}"
        )

        print(
            f"  Mismatched Fields: "
            f"{evidence_report['mismatched_fields']}"
        )

    else:

        print(
            "  Verification     : "
            "SECOND SOURCE UNAVAILABLE"
        )

    print("\n  OFFICIAL STATUS")
    print("  " + "-" * 66)

    if risk_report:

        print(
            f"  Status Level     : "
            f"{risk_report['risk_level']}"
        )

    else:

        print(
            "  Status Level     : "
            "NOT AVAILABLE"
        )

    print("\n")
    print("=" * 72)
    print("                  ANALYSIS COMPLETE")
    print("=" * 72)


def get_company_number():
    """Get company number from normal or demo mode."""

    if "--demo" in sys.argv:

        print("\n  DEMO MODE ENABLED")

        print(
            f"  Using demo company: "
            f"{DEMO_COMPANY_NUMBER}"
        )

        return DEMO_COMPANY_NUMBER

    return input(
        "\n  Enter Norwegian company number: "
    ).strip()


def get_primary_company(company_number):
    """
    Always try the live official API first.

    If the API cannot be reached, fall back to the
    saved 1,000+ company dataset.
    """

    print(
        "  → Querying official "
        "Brønnøysundregistrene API..."
    )

    try:

        api_company = get_company(
            company_number
        )

        if api_company:

            company = convert_api_company(
                api_company
            )

            print(
                "  ✓ Fresh official data retrieved."
            )

            return company

        print(
            "  → Company not returned by live API."
        )

    except Exception as error:

        print(
            "  ⚠ Live API lookup unavailable."
        )

        print(
            f"    Reason: {error}"
        )

    print(
        "  → Checking saved company dataset..."
    )

    saved_company = find_local_company(
        company_number
    )

    if saved_company:

        company = convert_saved_company(
            saved_company
        )

        print(
            "  ✓ Company found in saved dataset."
        )

        return company

    return None


def main():

    print_header()

    company_number = get_company_number()

    if not company_number.isdigit():

        print(
            "\n  ERROR: Company number "
            "must contain digits only."
        )

        return

    # ================================================================
    # STEP 1
    # ================================================================

    print_step(
        1,
        "PRIMARY COMPANY LOOKUP"
    )

    company = get_primary_company(
        company_number
    )

    if not company:

        print("\n")
        print("=" * 72)
        print("  COMPANY NOT FOUND")
        print("=" * 72)
        print(
            "\n  No company information was found "
            "for this organisation number."
        )

        return

    print_company_summary(
        company
    )

    display_company_status(
        company
    )

    # ================================================================
    # STEP 2
    # ================================================================

    print_step(
        2,
        "SECOND PUBLIC SOURCE"
    )

    print(
        "  → Searching second public source..."
    )

    try:

        second_source = get_proff_company(
            company_number
        )

        if second_source:

            print(
                "  ✓ Second-source evidence found."
            )

        else:

            print(
                "  ✗ Second-source evidence unavailable."
            )

        display_proff_source(
            second_source
        )

    except Exception as error:

        print(
            "  ✗ Second-source lookup failed."
        )

        print(
            f"    {error}"
        )

        second_source = None

    # ================================================================
    # STEP 3
    # ================================================================

    print_step(
        3,
        "CROSS-SOURCE EVIDENCE MATCHING"
    )

    evidence_report = None

    if second_source:

        print(
            "  → Comparing information "
            "between sources..."
        )

        try:

            evidence_report = (
                match_company_evidence(
                    company,
                    second_source
                )
            )

            display_evidence_report(
                evidence_report
            )

        except Exception as error:

            print(
                "  ✗ Evidence matching failed."
            )

            print(
                f"    {error}"
            )

    else:

        print(
            "  → Evidence comparison skipped."
        )

    # ================================================================
    # STEP 4
    # ================================================================

    print_step(
        4,
        "OFFICIAL STATUS ANALYSIS"
    )

    risk_report = None

    try:

        print(
            "  → Checking official "
            "company status..."
        )

        risk_report = analyze_company_risk(
            company
        )

        display_risk_report(
            risk_report
        )

    except Exception as error:

        print(
            "  ✗ Status analysis failed."
        )

        print(
            f"    {error}"
        )

    # ================================================================
    # STEP 5
    # ================================================================

    print_step(
        5,
        "FINAL SIGNALPOST REPORT"
    )

    display_final_summary(
        company,
        second_source,
        evidence_report,
        risk_report
    )


if __name__ == "__main__":
    main()