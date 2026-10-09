import argparse
import os

from dotenv import load_dotenv
from google import genai

SYSTEM_PROMPTS = {
    "summarize": """
You are a text summarization assistant.
Summarize the user's text concisely while preserving its
main ideas and important details.
Do not introduce new facts or change the original meaning.
Return only the summary.
""",

    "rewrite-formal": """
You are a professional writing assistant.
Rewrite the user's text in a professional and formal tone.
Correct grammar and improve clarity while preserving
the original meaning.
Do not invent information or change the user's intent.
Return only the rewritten text.
""",

    "explain-simple": """
You are a patient teacher who explains things to beginners.
Explain the user's text using simple, clear language.
Avoid unnecessary technical jargon.
Use a short example when it helps understanding.
Preserve the important meaning of the original text.
"""
}


FEW_SHOT_EXAMPLES = """
Example 1

Informal input: hey can you send me the report
Formal output: Could you please send me the report?

Example 2

Informal input: i need the files today so send them asap
Formal output: I would appreciate it if you could send me the files today as soon as possible.
"""

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=api_key)


def main():
    parser = argparse.ArgumentParser(
        description="CLI Writing Assistant"
    )

    parser.add_argument(
        "mode",
        choices=["summarize", "rewrite-formal", "explain-simple"],
        help="Writing mode to use"
    )

    parser.add_argument(
        "text",
        help="Text to process"
    )

    parser.add_argument(
        "--few-shot",
        action="store_true",
        help="Use examples for formal rewriting"
    )
    args = parser.parse_args()

    selected_prompt = SYSTEM_PROMPTS[args.mode]

    if args.few_shot and args.mode == "rewrite-formal":
        selected_prompt += "\n\n" + FEW_SHOT_EXAMPLES

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=args.text,
        config={
            "system_instruction": selected_prompt
        }
    )

    print(response.text)


if __name__ == "__main__":
    main()