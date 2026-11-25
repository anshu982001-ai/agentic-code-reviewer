
import re


def review_manager(code, security_review, bug_review, quality_review):
    """
    Combine agent findings into one consolidated report.
    Calculate risk level and remove duplicate findings.
    """

    reviews = [
        ("SECURITY", security_review),
        ("BUG", bug_review),
        ("CODE QUALITY", quality_review)
    ]

    findings = []
    seen = set()

    severity_rank = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3
    }

    highest_risk = "LOW"

    for agent_name, review in reviews:

        if not review:
            continue

        if "No runtime bugs detected." in review:
            continue

        if "No significant code quality issues found." in review:
            continue

        # Separate individual findings
        blocks = re.split(
            r"(?m)(?=^Severity\s*:)",
            review.strip()
        )

        for block in blocks:

            if not re.search(r"(?m)^Severity\s*:", block):
                continue

            # Remove duplicate findings
            normalized = re.sub(r"\s+", " ", block).strip()

            if normalized in seen:
                continue

            seen.add(normalized)

            severity_match = re.search(
                r"(?im)^Severity\s*:\s*(HIGH|MEDIUM|LOW)",
                block
            )

            if not severity_match:
                continue

            severity = severity_match.group(1).upper()

            if severity_rank[severity] > severity_rank[highest_risk]:
                highest_risk = severity

            category_match = re.search(
                r"(?im)^Category\s*:\s*(.+)",
                block
            )

            line_match = re.search(
                r"(?im)^Line\s*:\s*(.+)",
                block
            )

            description_match = re.search(
                r"(?im)^Description\s*:\s*(.+)",
                block
            )

            recommendation_match = re.search(
                r"(?im)^Recommendation\s*:\s*(.+)",
                block
            )

            findings.append({
                "severity": severity,
                "category": category_match.group(1).strip()
                    if category_match else agent_name,
                "line": line_match.group(1).strip()
                    if line_match else "Unknown",
                "description": description_match.group(1).strip()
                    if description_match else "No description provided",
                "recommendation": recommendation_match.group(1).strip()
                    if recommendation_match else "No recommendation provided"
            })

    # Generate final report
    report = [
        "# Code Review Summary",
        "",
        f"Overall Risk: {highest_risk}",
        "",
        "## Findings"
    ]

    if not findings:
        report.append("No issues detected.")
    else:
        for index, finding in enumerate(findings, start=1):
            report.extend([
                "",
                f"### {index}. {finding['severity']} - {finding['description']}",
                "",
                f"Category: {finding['category']}",
                f"Line: {finding['line']}",
                f"Description: {finding['description']}",
                f"Recommendation: {finding['recommendation']}"
            ])

    high_count = sum(
        1 for finding in findings
        if finding["severity"] == "HIGH"
    )

    medium_count = sum(
        1 for finding in findings
        if finding["severity"] == "MEDIUM"
    )

    report.extend([
        "",
        "## Summary",
        "",
        f"Total findings: {len(findings)}",
        f"HIGH severity: {high_count}",
        f"MEDIUM severity: {medium_count}",
        "",
        "Prioritize HIGH severity security issues, followed by MEDIUM severity bugs and code-quality issues."
    ])

    return "\n".join(report)
