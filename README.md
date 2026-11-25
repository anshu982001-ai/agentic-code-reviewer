# Agentic AI Code Reviewer

An AI-powered multi-agent code review system built using Python, LangGraph, LangChain, and Ollama. The application analyzes Python code for security vulnerabilities, potential bugs, and code quality issues.

## Features

- **Security Analysis:** Detects potential security vulnerabilities such as SQL injection.
- **Bug Detection:** Identifies potential runtime issues such as division by zero and missing dictionary keys.
- **Code Quality Analysis:** Reviews code for maintainability and coding practices.
- **Multi-Agent Workflow:** Uses LangGraph to coordinate specialized review agents.
- **Local LLM Integration:** Uses Qwen2.5-Coder 7B through Ollama.
- **Structured Reports:** Generates JSON reports with severity levels and recommendations.
- **Automated Testing:** Includes Pytest test cases for core functionality.

## Technology Stack

- Python
- LangChain
- LangGraph
- Ollama
- Qwen2.5-Coder 7B
- Pytest
- JSON

## Project Structure

```text
agentic-code-reviewer/
├── app/
│   ├── analyzer.py
│   ├── bug_reviewer.py
│   ├── github_client.py
│   ├── graph.py
│   ├── llm_reviewer.py
│   ├── quality_reviewer.py
│   ├── report_generator.py
│   ├── reviewer_manager.py
│   ├── security_reviewer.py
│   └── state.py
├── sample_code/
│   └── bad_code.py
├── reports/
│   └── review_report.json
├── tests/
│   └── test_reviewers.py
├── main.py
├── github_review.py
├── report_generator.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/anshu982001-ai/agentic-code-reviewer.git
cd agentic-code-reviewer
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama and download the model

Install Ollama from https://ollama.com, then run:

```bash
ollama pull qwen2.5-coder:7b
```

### 5. Run the application

```bash
python main.py
```

## Run Tests

```bash
python -m pytest tests/ -v
```

**Test Result:** 11 tests passed.

## Sample Review Findings

The sample code demonstrates detection of:

- SQL Injection
- Division by zero
- Missing dictionary keys
- Bare exception handling

The system generates structured review reports with severity classifications and recommendations.

## Future Enhancements

- FastAPI REST API integration
- Retrieval-Augmented Generation (RAG)
- Vector database integration
- Docker deployment
- Improved evaluation and reporting

## Author

**Anshu Singh**

GitHub: https://github.com/anshu982001-ai
