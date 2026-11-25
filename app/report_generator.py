
import re


def extract_findings(*reviews):
    findings = []

    for review in reviews:
        if not review:
            continue

        blocks = re.split(
            r"(?m)(?=^Severity\s*:)",
            review.strip()
        )

        for block in blocks:
            severity = re.search(
                r"(?im)^Severity\s*:\s*(HIGH|MEDIUM|LOW)",
                block
            )

            if not severity:
                continue

            def get_field(name):
                match = re.search(
                    rf"(?im)^{name}\s*:\s*(.*?)(?=^[A-Za-z_ ]+\s*:|\Z)",
                    block,
                    re.DOTALL
                )

                if not match:
                    return ""

                value = match.group(1).strip()

                # Remove Markdown code fences
                value = re.sub(
                    r"```(?:python)?\s*|\s*```",
                    "",
                    value
                )

                # Remove Python label after "For example:"
                value = re.sub(
                    r"(?i):[ \t]*python[ \t]*\n",
                    ":\n",
                    value
                )

                # Remove standalone Python label
                value = re.sub(
                    r"(?m)^\s*python\s*$",
                    "",
                    value
                ).strip()

                return value

            line_value = get_field("Line")

            findings.append({
                "severity": severity.group(1).upper(),
                "category": get_field("Category"),
                "line": int(line_value) if line_value.isdigit() else None,
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
        level: sum(
            1 for item in findings
            if item["severity"] == level
        )
        for level in ["HIGH", "MEDIUM", "LOW"]
    }

    if severity_counts["HIGH"]:
        overall_risk = "HIGH"
    elif severity_counts["MEDIUM"]:
        overall_risk = "MEDIUM"
    else:
        overall_risk = "LOW"

    return {
        "project": "Agentic Code Reviewer",
        "source_file": str(source_file),
        "overall_risk": overall_risk,
        "total_findings": len(findings),
        "severity_counts": severity_counts,
        "findings": findings
    }


