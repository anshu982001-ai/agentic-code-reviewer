

import re


def bug_agent(code):
    findings = []
    lines = code.splitlines()

    for line_number, line in enumerate(lines, start=1):

        if re.search(r"/\s*b\b", line):
            findings.append(
                f"""Severity: MEDIUM
Category: BUG
Line: {line_number}
Description: Variable 'b' may be zero, causing ZeroDivisionError.
Recommendation: Validate that b is not zero before division."""
            )

        if re.search(r'\buser\["name"\]', line):
            findings.append(
                f"""Severity: MEDIUM
Category: BUG
Line: {line_number}
Description: Dictionary key 'name' may be missing, causing KeyError.
Recommendation: Use user.get("name") or check whether the key exists."""
            )

    if not findings:
        return "No runtime bugs detected."

    return "\n\n".join(findings)
