from langchain_ollama import ChatOllama


# Local Qwen2.5-Coder model through Ollama
llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0
)


def security_agent(code):
    """
    Analyze Python code specifically for security vulnerabilities.
    """

    prompt = f"""
You are an expert application security code reviewer.

Analyze the Python code below ONLY for genuine security vulnerabilities.

Look for these security issues:

1. SQL Injection
2. Command Injection
3. Hardcoded passwords, API keys, or secrets
4. Authentication vulnerabilities
5. Authorization vulnerabilities
6. Path Traversal
7. Unsafe Deserialization
8. Insecure File Operations
9. Sensitive Information Exposure
10. Server-Side Request Forgery (SSRF)
11. Dangerous use of eval(), exec(), or similar functions

IMPORTANT RULES:

- Only report vulnerabilities that are supported by the provided code.
- Do NOT invent vulnerabilities.
- Do NOT report "not applicable" categories.
- Do NOT report normal programming bugs.
- Do NOT report performance issues.
- Do NOT report general code-quality issues.
- If a vulnerability is not present, simply ignore it.
- If there are no security vulnerabilities, respond with:
  "No confirmed security vulnerabilities found."

For every confirmed security vulnerability, use this format:

Severity: HIGH / MEDIUM / LOW
Category: <security category>
Line: <line number if known>
Description: <explain the vulnerability>
Recommendation: <explain how to fix it>

Keep the response concise.

Here is the Python code:

{code}
"""

    # Show the code being sent to the AI.
    # This is useful while we are developing and debugging.
    print("\n--- CODE SENT TO SECURITY AGENT ---")
    print(code)
    print("-----------------------------------")

    # Send the prompt to Qwen through Ollama
    response = llm.invoke(prompt)

    # Return the AI-generated security review
    return response.content