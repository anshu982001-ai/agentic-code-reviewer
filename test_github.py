from app.github_client import get_changed_files


REPO_NAME =  "anshu982001-ai/Swiggy-Analysis-Project1"
PR_NUMBER = 1


files = get_changed_files(
    REPO_NAME,
    PR_NUMBER
)


print("\nGitHub Pull Request Files")
print("=========================")


for file in files:
    print("\nFile:", file["filename"])
    print("Status:", file["status"])
    print("Changes:", file["changes"])
    print("Patch:")
    print(file["patch"])