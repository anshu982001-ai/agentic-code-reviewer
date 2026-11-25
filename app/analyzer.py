
def analyze_code(code):
    issues = []

    lines = code.splitlines()

    for line_number, line in enumerate(lines, start=1):

        # Check for possible SQL injection
        if "SELECT" in line and "+" in line:
            issues.append({
                "severity": "HIGH",
                "category": "SECURITY",
                "line": line_number,
                "title": "Possible SQL Injection",
                "description": "SQL query appears to use string concatenation with user input.",
                "recommendation": "Use parameterized queries instead of string concatenation."
            })

        # Check for bare except
        if line.strip() == "except:":
            issues.append({
                "severity": "MEDIUM",
                "category": "CODE QUALITY",
                "line": line_number,
                "title": "Bare Exception Handler",
                "description": "A bare except catches all exceptions.",
                "recommendation": "Catch specific exception types."
            })

        # Check for division
        if "/" in line and "def " not in line:
            issues.append({
                "severity": "MEDIUM",
                "category": "POTENTIAL BUG",
                "line": line_number,
                "title": "Possible Division by Zero",
                "description": "Division may fail if the denominator is zero.",
                "recommendation": "Validate the denominator before performing division."
            })

    return issues