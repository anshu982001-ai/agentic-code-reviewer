from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0
)


def review_with_ai(code):
    prompt = f"""
You are an expert software code reviewer.

Review the following Python code.

Identify:
1. Security vulnerabilities
2. Bugs and potential runtime errors
3. Code quality problems
4. Performance problems
5. Recommended improvements

For every important issue, provide:
- Severity
- Category
- Explanation
- Recommended fix

Be specific and concise.

Code to review:

{code}
"""

    response = llm.invoke(prompt)

    return response.content