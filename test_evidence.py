from agent.evidence_matcher import (
    match_company_evidence,
    display_evidence_report
)


brreg_company = {
    "company_number": "923609016",
    "company_name": "EQUINOR ASA",
    "registration_date": "1995-03-12",
    "foundation_date": "1972-09-18",
    "industry_code": "06.100",
    "postal_code": "4035",
    "city": "STAVANGER",
    "municipality": "STAVANGER"
}


second_source_company = {
    "company_number": "923609016",
    "company_name": "EQUINOR ASA",
    "registration_date": "1995-03-12",
    "foundation_date": "1972-09-18",
    "industry_code": "06.100",
    "postal_code": "4035",
    "city": "STAVANGER",
    "municipality": "STAVANGER"
}


print("\nStarting SignalPost evidence test...")

report = match_company_evidence(
    brreg_company,
    second_source_company
)

display_evidence_report(
    report
)