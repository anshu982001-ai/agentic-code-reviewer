

import json
from pathlib import Path

from app.graph import review_graph
from app.report_generator import generate_report


print("Agentic Code Reviewer started!")

# Read sample Python code
file_path = Path("sample_code/bad_code.py")

if not file_path.exists():
    raise FileNotFoundError(
        f"Sample file not found: {file_path}"
    )

code = file_path.read_text(encoding="utf-8")

# Initialize LangGraph state
initial_state = {
    "code": code,
    "security_review": "",
    "bug_review": "",
    "quality_review": "",
    "final_review": ""
}

print("\nStarting multi-agent code review...")

# Execute LangGraph workflow
result = review_graph.invoke(initial_state)

# Display individual agent reports
reviews = {
    "SECURITY REVIEW": result["security_review"],
    "BUG REVIEW": result["bug_review"],
    "QUALITY REVIEW": result["quality_review"],
    "FINAL CONSOLIDATED REVIEW": result["final_review"]
}

for title, review in reviews.items():
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(review)

# Generate structured JSON report
report = generate_report(result, file_path)

# Create reports directory
reports_dir = Path("reports")
reports_dir.mkdir(parents=True, exist_ok=True)

# Save JSON report
report_path = reports_dir / "review_report.json"

with report_path.open("w", encoding="utf-8") as file:
    json.dump(
        report,
        file,
        indent=4,
        ensure_ascii=False
    )

print("\n" + "=" * 60)
print("STRUCTURED JSON REPORT GENERATED")
print("=" * 60)

print(f"Total findings: {report['total_findings']}")
print(f"Overall risk: {report['overall_risk']}")
print(f"HIGH: {report['severity_counts']['HIGH']}")
print(f"MEDIUM: {report['severity_counts']['MEDIUM']}")
print(f"LOW: {report['severity_counts']['LOW']}")

print(f"\nReport saved at: {report_path.resolve()}")

print("\nCode review completed!")
