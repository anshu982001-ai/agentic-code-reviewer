from app.github_client import get_changed_files, post_pr_comment
from app.graph import review_graph


REPO_NAME = "anshu982001-ai/Swiggy-Analysis-Project1"
PR_NUMBER = 1


def main():
    print("Agentic GitHub Code Reviewer started!")

    files = get_changed_files(
        REPO_NAME,
        PR_NUMBER
    )

    if not files:
        print("No changed files found.")
        return

    for file in files:
        filename = file["filename"]

        # Only review Python files
        if not filename.endswith(".py"):
            continue

        print("\n" + "=" * 60)
        print("REVIEWING:", filename)
        print("=" * 60)

        # Get complete file content
        code = file.get("content")

        if not code:
            print("Could not retrieve file content.")
            continue

        # Send complete source code to the agentic review graph
        result = review_graph.invoke({
            "code": code
        })

        print("\n--- SECURITY REVIEW ---")
        print(result.get("security_review", ""))

        print("\n--- BUG REVIEW ---")
        print(result.get("bug_review", ""))

        print("\n--- QUALITY REVIEW ---")
        print(result.get("quality_review", ""))

        # Get final review
        final_review = result.get("final_review", "")

        print("\n--- FINAL CODE REVIEW ---")
        print(final_review)

        # Post final review to GitHub PR
        if final_review:
            comment = f"""## 🤖 Agentic Code Review

**File:** `{filename}`

{final_review}
"""

            post_pr_comment(
                REPO_NAME,
                PR_NUMBER,
                comment
            )


if __name__ == "__main__":
    main()