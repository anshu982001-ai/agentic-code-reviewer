# from langgraph.graph import StateGraph, START, END

# from app.state import ReviewState
# from app.analyzer import analyze_code
# from app.llm_reviewer import review_with_ai


# def static_analysis_node(state: ReviewState):
#     issues = analyze_code(state["code"])

#     return {
#         "issues": issues
#     }


# def ai_review_node(state: ReviewState):
#     ai_review = review_with_ai(state["code"])

#     return {
#         "ai_review": ai_review
#     }


# builder = StateGraph(ReviewState)

# builder.add_node("static_analysis", static_analysis_node)
# builder.add_node("ai_review", ai_review_node)

# builder.add_edge(START, "static_analysis")
# builder.add_edge("static_analysis", "ai_review")
# builder.add_edge("ai_review", END)

# review_graph = builder.compile()

# from langgraph.graph import StateGraph, START, END

# from app.state import ReviewState
# from app.security_reviewer import security_agent
# from app.bug_reviewer import bug_agent
# from app.quality_reviewer import quality_agent


# def security_node(state: ReviewState):
#     result = security_agent(state["code"])

#     return {
#         "security_review": result
#     }


# def bug_node(state: ReviewState):
#     result = bug_agent(state["code"])

#     return {
#         "bug_review": result
#     }


# def quality_node(state: ReviewState):
#     result = quality_agent(state["code"])

#     return {
#         "quality_review": result
#     }


# builder = StateGraph(ReviewState)

# builder.add_node("security", security_node)
# builder.add_node("bugs", bug_node)
# builder.add_node("quality", quality_node)

# builder.add_edge(START, "security")
# builder.add_edge("security", "bugs")
# builder.add_edge("bugs", "quality")
# builder.add_edge("quality", END)

# review_graph = builder.compile()

from langgraph.graph import StateGraph, START, END

from app.state import ReviewState
from app.security_reviewer import security_agent
from app.bug_reviewer import bug_agent
from app.quality_reviewer import quality_agent
from app.reviewer_manager import review_manager


def security_node(state: ReviewState):
    result = security_agent(state["code"])

    return {
        "security_review": result
    }


def bug_node(state: ReviewState):
    result = bug_agent(state["code"])

    return {
        "bug_review": result
    }


def quality_node(state: ReviewState):
    result = quality_agent(state["code"])

    return {
        "quality_review": result
    }


def manager_node(state: ReviewState):
    result = review_manager(
        state["code"],
        state["security_review"],
        state["bug_review"],
        state["quality_review"]
    )

    return {
        "final_review": result
    }


builder = StateGraph(ReviewState)

builder.add_node("security", security_node)
builder.add_node("bugs", bug_node)
builder.add_node("quality", quality_node)
builder.add_node("manager", manager_node)

builder.add_edge(START, "security")
builder.add_edge("security", "bugs")
builder.add_edge("bugs", "quality")
builder.add_edge("quality", "manager")
builder.add_edge("manager", END)

review_graph = builder.compile()