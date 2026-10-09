# CLI Writing Assistant

A command-line writing assistant built with Python and Google's Gemini API. It uses prompt engineering to summarize text, rewrite informal text in a professional tone, and explain concepts in simple language.

## Features

* **Summarize:** Produces concise summaries while preserving key information.
* **Rewrite Formal:** Improves grammar, clarity, and professionalism while preserving the original meaning.
* **Explain Simple:** Explains text in beginner-friendly language.
* **Few-Shot Prompting:** Supports two examples for formal rewriting through the `--few-shot` flag.
* **Token Usage Logging:** Displays token usage reported by Gemini.
* **Retry and Error Handling:** Retries selected API errors and request timeouts, then displays a helpful message if the request still fails.

## Technologies Used

* Python
* Google Gemini API
* Google GenAI Python SDK
* python-dotenv
* httpx

## Prerequisites

* Python 3.11 or later
* A Google Gemini API key
* Git (optional, for cloning the repository)

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/MindfullLearner/CLI-Writing-Assistant.git
cd CLI-Writing-Assistant
```

Alternatively, download the repository and open its folder in VS Code.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install google-genai python-dotenv httpx
```

### 4. Configure the API key

Create a file named `.env` in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own API key.

**Security:** Never commit your actual API key or share it publicly. The `.env` file should remain excluded through `.gitignore`.

## Usage

Run commands from the project directory with the virtual environment activated.

### Summarize text

```bash
python assistant.py summarize "Artificial intelligence helps computers perform tasks that normally require human intelligence."
```

### Rewrite text formally

```bash
python assistant.py rewrite-formal "hey can you send me the report"
```

### Rewrite using few-shot prompting

```bash
python assistant.py rewrite-formal --few-shot "hey can you send me the report"
```

### Explain text simply

```bash
python assistant.py explain-simple "Explain how machine learning works."
```

After a successful request, the program displays the generated response and available token-usage metadata.

## Project Structure

```text
CLI-Writing-Assistant/
├── assistant.py
├── test_gemini.py
├── PROMPTS.md
├── README.md
├── COMPARISON.md
├── .gitignore
└── .env                 # Local only; not committed
```

The `.venv/` and `__pycache__/` directories are also local and should not be committed.

## Error Handling

The application retries selected API errors, including HTTP 429 and temporary server errors, using increasing wait times. It also retries HTTP request timeouts. If the attempts fail, it displays a user-friendly error message.

Retries cannot guarantee recovery from exhausted API quotas or persistent service failures.

## Documentation

* `PROMPTS.md` describes the system prompts, prompt-design principles, few-shot examples, and token-usage logging.
* `COMPARISON.md` compares the behavior of standard prompting and few-shot prompting.

## Limitations

* A working Gemini API key and available API quota are required.
* Output quality and token counts may vary between requests.
* The few-shot comparison is based on example tests and does not prove that few-shot prompting is always better.

## Learning Objectives

This project demonstrates practical use of prompt engineering, command-line argument parsing, external API integration, token-usage metadata, environment variables, and retry/error handling.
