
import re


def extract_findings(*reviews):
    findings = []

    for review in reviews:
        if not review:
            continue

        # Split report into individual findings
        blocks = re.split(
            r"(?m)(?=^Severity\s*:)",
            review.strip()
        )

        for block in blocks:

            severity_match = re.search(
                r"(?im)^Severity\s*:\s*(HIGH|MEDIUM|LOW)",
                block
            )

            if not severity_match:
                continue

            def get_field(field_name):
                pattern = rf"(?im)^{field_name}\s*:\s*(.*?)(?=^[A-Za-z_ ]+\s*:|\Z)"

                match = re.search(
                    pattern,
                    block,
                    re.MULTILINE | re.DOTALL
                )

                if match:
                    value = match.group(1).strip()

                    # Remove Markdown code blocks from field text
                    value = re.sub(
                        r"```(?:python)?\s*|\s*```",
                        "",
                        value
                    ).strip()

                    return value

                return ""

            findings.append({
                "severity": severity_match.group(1).upper(),
                "category": get_field("Category"),
                "line": get_field("Line"),
                "description": get_field("Description"),
                "recommendation": get_field("Recommendation")
            })

    return findings


def generate_report(result, source_file):

    findings = extract_findings(
        result.get("security_review", ""),
        result.get("bug_review", ""),
        result.get("quality_review", "")
    )

    severity_counts = {
        "HIGH": sum(
            1 for finding in findings
            if finding["severity"] == "HIGH"
        ),
        "MEDIUM": sum(
            1 for finding in findings
            if finding["severity"] == "MEDIUM"
        ),
        "LOW": sum(
            1 for finding in findings
            if finding["severity"] == "LOW"
        )
    }

    if severity_counts["HIGH"] > 0:
        overall_risk = "HIGH"
    elif severity_counts["MEDIUM"] > 0:
        overall_risk = "MEDIUM"
    else:
        overall_risk = "LOW"

    report = {
        "project": "Agentic Code Reviewer",
        "source_file": str(source_file),
        "overall_risk": overall_risk,
        "total_findings": len(findings),
        "severity_counts": severity_counts,
        "findings": findings
    }

    return report
