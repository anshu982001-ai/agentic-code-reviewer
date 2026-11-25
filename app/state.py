# from typing import TypedDict


# class ReviewState(TypedDict):
    # code: str
    # issues: list
    # ai_review: str

# from typing import TypedDict


# class ReviewState(TypedDict):
#     code: str
#     security_review: str
#     bug_review: str
#     quality_review: str
#     final_review: str

from typing import TypedDict


class ReviewState(TypedDict):
    code: str
    security_review: str
    bug_review: str
    quality_review: str
    final_review: str