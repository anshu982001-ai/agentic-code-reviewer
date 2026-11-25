import os

from dotenv import load_dotenv
from github import Github, Auth


load_dotenv()


def get_github_client():
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise ValueError(
            "GITHUB_TOKEN is missing. Check your .env file."
        )

    auth = Auth.Token(token)

    return Github(auth=auth)


def get_pull_request(repo_name, pr_number):
    github = get_github_client()

    repo = github.get_repo(repo_name)

    return repo.get_pull(pr_number)


def get_changed_files(repo_name, pr_number):
    pull_request = get_pull_request(repo_name, pr_number)

    files = []

    for file in pull_request.get_files():

        file_content = None

        try:
            content_file = pull_request.base.repo.get_contents(
                file.filename,
                ref=pull_request.head.sha
            )

            file_content = content_file.decoded_content.decode("utf-8")

        except Exception as e:
            print(
                f"Could not retrieve complete content "
                f"for {file.filename}: {e}"
            )

        files.append({
            "filename": file.filename,
            "status": file.status,
            "additions": file.additions,
            "deletions": file.deletions,
            "changes": file.changes,
            "patch": file.patch,
            "content": file_content
        })

    return files


def post_pr_comment(repo_name, pr_number, comment):
    pull_request = get_pull_request(repo_name, pr_number)

    pull_request.create_issue_comment(comment)

    print("Review posted to GitHub successfully.")