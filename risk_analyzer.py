def analyze_company_risk(company):
    """
    Analyze official company status information.

    This is a rule-based status check.
    It does not make financial or legal predictions.
    """

    findings = []
    risk_level = "LOW"

    bankrupt = company.get("bankrupt")
    under_liquidation = company.get("under_liquidation")

    # Bankruptcy check
    if bankrupt is True:
        findings.append({
            "type": "CRITICAL",
            "field": "Bankrupt",
            "message": "Company is marked as bankrupt in the official source."
        })
        risk_level = "HIGH"

    # Liquidation check
    if under_liquidation is True:
        findings.append({
            "type": "WARNING",
            "field": "Under Liquidation",
            "message": "Company is marked as under liquidation in the official source."
        })

        if risk_level != "HIGH":
            risk_level = "MEDIUM"

    # Normal status
    if bankrupt is False and under_liquidation is False:
        findings.append({
            "type": "INFO",
            "field": "Company Status",
            "message": "No bankruptcy or liquidation flag was found in the official source."
        })

    # Missing information
    if bankrupt is None:
        findings.append({
            "type": "INFO",
            "field": "Bankrupt",
            "message": "Bankruptcy status was not available."
        })

    if under_liquidation is None:
        findings.append({
            "type": "INFO",
            "field": "Under Liquidation",
            "message": "Liquidation status was not available."
        })

    return {
        "risk_level": risk_level,
        "findings": findings
    }


def display_risk_report(report):
    print("\n")
    print("=" * 70)
    print("                 SIGNALPOST COMPANY STATUS")
    print("=" * 70)

    print("\n[STATUS ASSESSMENT]")
    print("-" * 70)

    print(f"Status Level        : {report['risk_level']}")

    print("\n[STATUS FINDINGS]")
    print("-" * 70)

    for finding in report["findings"]:
        print(f"{finding['type']:<10} | {finding['field']}")
        print(f"           {finding['message']}")

    print("\n")
    print("=" * 70)