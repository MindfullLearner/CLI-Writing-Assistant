import argparse
import os
import time
import httpx

from dotenv import load_dotenv
from google import genai
from google.genai import errors

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

    try:
        response = generate_with_retry(args.text, selected_prompt)

    except errors.APIError as exc:
        status_code = getattr(exc, "code", None)

        if status_code == 429:
            print("Error: Gemini rate limit or quota reached. Please try again later.")
        elif status_code in {500, 502, 503, 504}:
            print("Error: Gemini is temporarily unavailable. Please try again later.")
        else:
            print(f"Error: Gemini API request failed. Details: {exc}")

        return

    except httpx.TimeoutException:
        print("Error: The request timed out after multiple attempts. Please try again.")
        return

    
    print(response.text)

    
    usage = response.usage_metadata

    if usage:
        input_tokens = usage.prompt_token_count or 0
        output_tokens = usage.candidates_token_count or 0
        thought_tokens = usage.thoughts_token_count or 0
        total_tokens = usage.total_token_count or 0

        print("\n--- Token Usage ---")
        print(f"Input tokens: {input_tokens}")
        print(f"Output tokens: {output_tokens}")
        print(f"Thought tokens: {thought_tokens}")
        print(f"Total tokens reported by Gemini: {total_tokens}")
    else:
        print("\nToken usage metadata is unavailable.")


def generate_with_retry(text, selected_prompt, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            return client.models.generate_content(
                model="gemini-3.8-flash",
                contents=text,
                config={
                    "system_instruction": selected_prompt
                }
            )

        except errors.APIError as exc:
            status_code = getattr(exc, "code", None)

            if status_code is None:
                status_code = getattr(exc, "status_code", None)

            retryable_codes = {429, 500, 502, 503, 504}

            if status_code not in retryable_codes:
                raise

            if attempt == max_attempts:
                raise

            wait_seconds = 2 ** attempt

            print(
                f"Gemini API error {status_code}. "
                f"Retrying in {wait_seconds} seconds "
                f"(attempt {attempt + 1}/{max_attempts})..."
            )
            time.sleep(wait_seconds)

        except httpx.TimeoutException:
            if attempt == max_attempts:
                raise

            wait_seconds = 2 ** attempt

            print(
                f"Request timed out. Retrying in {wait_seconds} seconds "
                f"(attempt {attempt + 1}/{max_attempts})..."
            )
            time.sleep(wait_seconds)
if __name__ == "__main__":
    main()
    