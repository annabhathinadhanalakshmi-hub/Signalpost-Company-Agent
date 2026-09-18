import re


def normalize(value):
    """
    Normalize general text before comparison.
    """

    if value is None:
        return ""

    value = str(value).strip().lower()

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value


def normalize_company_name(value):
    """
    Normalize company names.
    """

    value = normalize(value)

    value = re.sub(
        r"[.,]",
        "",
        value
    )

    return value


def normalize_website(value):
    """
    Normalize website values.
    """

    value = normalize(value)

    value = value.replace(
        "https://",
        ""
    )

    value = value.replace(
        "http://",
        ""
    )

    value = value.replace(
        "www.",
        ""
    )

    return value.rstrip("/")


def normalize_phone(value):
    """
    Normalize phone numbers.
    """

    if value is None:
        return ""

    return re.sub(
        r"\D",
        "",
        str(value)
    )


def get_normalized_value(
    field_name,
    value
):

    if field_name == "company_name":

        return normalize_company_name(
            value
        )

    if field_name == "website":

        return normalize_website(
            value
        )

    if field_name == "phone":

        return normalize_phone(
            value
        )

    return normalize(value)


def compare_field(
    field_name,
    source_a,
    source_b
):

    value_a = get_normalized_value(
        field_name,
        source_a.get(field_name)
    )

    value_b = get_normalized_value(
        field_name,
        source_b.get(field_name)
    )

    if not value_a or not value_b:

        return {
            "field": field_name,
            "status": "NOT_AVAILABLE",
            "source_a": value_a,
            "source_b": value_b
        }

    if value_a == value_b:

        return {
            "field": field_name,
            "status": "MATCH",
            "source_a": value_a,
            "source_b": value_b
        }

    return {
        "field": field_name,
        "status": "MISMATCH",
        "source_a": value_a,
        "source_b": value_b
    }


def calculate_verification_status(
    matched,
    mismatched,
    unavailable
):
    """
    Determine a descriptive verification status.

    This is based only on the available
    cross-source comparisons.
    """

    available = (
        matched + mismatched
    )

    if available == 0:

        return "INSUFFICIENT EVIDENCE"

    match_rate = (
        matched / available
    ) * 100

    if mismatched > 0:

        return "REVIEW REQUIRED"

    if matched >= 3:

        return "CROSS-SOURCE MATCH"

    return "PARTIAL MATCH"


def match_company_evidence(
    primary_company,
    secondary_company
):

    fields = [
        "company_number",
        "company_name",
        "registration_date",
        "foundation_date",
        "industry_code",
        "employees",
        "website",
        "postal_code",
        "city",
        "municipality"
    ]

    results = []

    for field in fields:

        result = compare_field(
            field,
            primary_company,
            secondary_company
        )

        results.append(result)

    matched = 0
    mismatched = 0
    unavailable = 0

    for result in results:

        if result["status"] == "MATCH":

            matched += 1

        elif result["status"] == "MISMATCH":

            mismatched += 1

        else:

            unavailable += 1

    total_fields = len(fields)

    available_fields = (
        matched + mismatched
    )

    if total_fields > 0:

        coverage = (
            available_fields /
            total_fields
        ) * 100

    else:

        coverage = 0

    if available_fields > 0:

        match_rate = (
            matched /
            available_fields
        ) * 100

    else:

        match_rate = 0

    verification_status = (
        calculate_verification_status(
            matched,
            mismatched,
            unavailable
        )
    )

    return {
        "results": results,

        "matched_fields":
            matched,

        "mismatched_fields":
            mismatched,

        "unavailable_fields":
            unavailable,

        "total_fields":
            total_fields,

        "coverage":
            round(
                coverage,
                2
            ),

        "match_rate":
            round(
                match_rate,
                2
            ),

        "verification_status":
            verification_status
    }


def display_evidence_report(report):

    print("\n")
    print("=" * 70)
    print("                 SIGNALPOST EVIDENCE REPORT")
    print("=" * 70)

    print("\n[FIELD COMPARISON]")

    print("-" * 70)

    for result in report["results"]:

        print(
            f"{result['field']:<22} : "
            f"{result['status']}"
        )

        if result["source_a"]:

            print(
                f"  Primary Source : "
                f"{result['source_a']}"
            )

        if result["source_b"]:

            print(
                f"  Second Source  : "
                f"{result['source_b']}"
            )

    print("\n[SUMMARY]")

    print(
        f"Total fields         : "
        f"{report['total_fields']}"
    )

    print(
        f"Matched fields       : "
        f"{report['matched_fields']}"
    )

    print(
        f"Mismatched fields    : "
        f"{report['mismatched_fields']}"
    )

    print(
        f"Unavailable fields   : "
        f"{report['unavailable_fields']}"
    )

    print(
        f"Evidence coverage    : "
        f"{report['coverage']}%"
    )

    print(
        f"Available-field match: "
        f"{report['match_rate']}%"
    )

    print(
        f"Verification status  : "
        f"{report['verification_status']}"
    )

    print("\n[INTERPRETATION]")

    if report["verification_status"] == (
        "REVIEW REQUIRED"
    ):

        print(
            "Some available fields differ "
            "between the sources."
        )

    elif report["verification_status"] == (
        "CROSS-SOURCE MATCH"
    ):

        print(
            "Multiple available fields "
            "match across both sources."
        )

    elif report["verification_status"] == (
        "PARTIAL MATCH"
    ):

        print(
            "The available fields match, "
            "but more evidence is needed."
        )

    else:

        print(
            "There is not enough information "
            "for a cross-source comparison."
        )

    print("\n" + "=" * 70)