
from app.security_reviewer import security_agent
from app.quality_reviewer import quality_agent


# Mock response for Security Agent
class MockResponse:
    content = """Severity: HIGH
Category: SQL Injection
Line: 2
Description: SQL query uses unsafe string concatenation.
Recommendation: Use parameterized queries."""


class MockLLM:
    def invoke(self, prompt):
        return MockResponse()


# -------------------------------
# SECURITY AGENT TESTS
# -------------------------------

def test_security_agent_detects_sql_injection(monkeypatch):

    import app.security_reviewer as security_module

    monkeypatch.setattr(
        security_module,
        "llm",
        MockLLM()
    )

    code = """
def get_user(user_id):
    query = "SELECT * FROM users WHERE id=" + user_id
    return db.execute(query)
"""

    result = security_agent(code)

    assert "SQL Injection" in result
    assert "HIGH" in result


def test_security_agent_receives_python_code(monkeypatch):

    import app.security_reviewer as security_module

    class PromptCheckingLLM:
        def invoke(self, prompt):
            assert "def calculate(a, b):" in prompt
            return MockResponse()

    monkeypatch.setattr(
        security_module,
        "llm",
        PromptCheckingLLM()
    )

    code = "def calculate(a, b):\n    return a + b"

    result = security_agent(code)

    assert result is not None


# -------------------------------
# QUALITY AGENT TESTS
# -------------------------------

def test_quality_agent_detects_bare_exception():

    code = """
def process():
    try:
        print("Hello")
    except:
        pass
"""

    result = quality_agent(code)

    assert "CODE_QUALITY" in result
    assert "MEDIUM" in result
    assert "silently ignores exceptions" in result


def test_quality_agent_returns_no_issue_for_clean_code():

    code = """
def add(a, b):
    return a + b
"""

    result = quality_agent(code)

    assert result == "No significant code quality issues found."


def test_quality_agent_allows_specific_exception():

    code = """
def process():
    try:
        print("Hello")
    except ValueError:
        print("Invalid value")
"""

    result = quality_agent(code)

    assert result == "No significant code quality issues found."


from app.bug_reviewer import bug_agent


def test_bug_agent_detects_division_by_zero():

    code = """
def divide(a, b):
    return a / b
"""

    result = bug_agent(code)

    assert "ZeroDivisionError" in result
    assert "MEDIUM" in result


def test_bug_agent_detects_missing_dictionary_key():

    code = """
def process_user(user):
    print(user["name"])
"""

    result = bug_agent(code)

    assert "KeyError" in result
    assert "MEDIUM" in result


def test_bug_agent_returns_no_issue_for_clean_code():

    code = """
def add(a, b):
    return a + b
"""

    result = bug_agent(code)

    assert result == "No runtime bugs detected."



from app.report_generator import generate_report


def test_report_generator_counts_findings():

    result = {
        "security_review": """Severity: HIGH
Category: SQL Injection
Line: 2
Description: Unsafe SQL query.
Recommendation: Use parameterized queries.""",

        "bug_review": """Severity: MEDIUM
Category: BUG
Line: 7
Description: Division by zero possible.
Recommendation: Validate b before division.""",

        "quality_review": """Severity: MEDIUM
Category: CODE_QUALITY
Line: 13
Description: Bare exception handling.
Recommendation: Catch specific exceptions."""
    }

    report = generate_report(result, "sample_code/bad_code.py")

    assert report["total_findings"] == 3
    assert report["overall_risk"] == "HIGH"
    assert report["severity_counts"]["HIGH"] == 1
    assert report["severity_counts"]["MEDIUM"] == 2
    assert report["severity_counts"]["LOW"] == 0


def test_report_generator_uses_integer_line_numbers():

    result = {
        "security_review": """Severity: HIGH
Category: SQL Injection
Line: 2
Description: Unsafe SQL query.
Recommendation: Use parameterized queries.""",
        "bug_review": "",
        "quality_review": ""
    }

    report = generate_report(result, "sample.py")

    assert report["findings"][0]["line"] == 2
    assert isinstance(report["findings"][0]["line"], int)


def test_report_generator_cleans_recommendation():

    result = {
        "security_review": """Severity: HIGH
Category: SQL Injection
Line: 2
Description: Unsafe SQL query.
Recommendation: For example:python
query = "SELECT * FROM users WHERE id=%s"
return db.execute(query, (user_id,))""",
        "bug_review": "",
        "quality_review": ""
    }

    report = generate_report(result, "sample.py")

    recommendation = report["findings"][0]["recommendation"]

    assert "python" not in recommendation.lower()
    assert "parameterized" not in recommendation.lower()
    assert "query =" in recommendation
