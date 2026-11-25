
import re


def quality_agent(code):
    findings = []
    lines = code.splitlines()

    for index, line in enumerate(lines):

        if re.match(r"^\s*except\s*:", line):

            next_line = (
                lines[index + 1]
                if index + 1 < len(lines)
                else ""
            )

            if re.match(r"^\s*pass\s*(#.*)?$", next_line):
                findings.append(
                    f"""Severity: MEDIUM
Category: CODE_QUALITY
Line: {index + 1}
Description: Bare exception handling silently ignores exceptions using pass.
Recommendation: Catch specific exceptions and log or handle them appropriately."""
                )

    if not findings:
        return "No significant code quality issues found."

    return "\n\n".join(findings)
