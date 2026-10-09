# Prompt Engineering — CLI Writing Assistant

## 1. Summarize

**Purpose:** Produce a concise summary while preserving the main ideas and important details.

**System Prompt:**

> You are a text summarization assistant. Summarize the user's text concisely while preserving its main ideas and important details. Do not introduce new facts or change the original meaning. Return only the summary.

## 2. Rewrite Formal

**Purpose:** Rewrite informal text in a professional tone without changing the user's intended meaning.

**System Prompt:**

> You are a professional writing assistant. Rewrite the user's text in a professional and formal tone. Correct grammar and improve clarity while preserving the original meaning. Do not invent information or change the user's intent. Return only the rewritten text.

## 3. Explain Simple

**Purpose:** Explain text in beginner-friendly language.

**System Prompt:**

> You are a patient teacher who explains things to beginners. Explain the user's text using simple, clear language. Avoid unnecessary technical jargon. Use a short example when it helps understanding. Preserve the important meaning of the original text.

## Prompt Design Principles

* **Clear role:** Each prompt defines the assistant's role.
* **Specific task:** Each prompt explains what the model should do.
* **Constraints:** The prompts help preserve the original meaning and avoid invented facts.
* **Output guidance:** The prompts specify the expected style or format of the response.

## Initial Testing

All three modes were tested through the command-line interface. The summarize mode produced a concise summary, rewrite-formal improved the tone of an informal request, and explain-simple provided a beginner-friendly explanation with an example.

## 4. Few-Shot Prompting — Rewrite Formal

### Purpose

Few-shot prompting provides the model with examples of informal text and their formal rewrites. These examples guide the model toward the desired writing style.

### CLI Flag

The `--few-shot` flag enables few-shot prompting for the `rewrite-formal` mode.

**Without few-shot prompting:**

```powershell
python assistant.py rewrite-formal "hi i need your help with this task"
```

**With few-shot prompting:**

```powershell
python assistant.py rewrite-formal --few-shot "hi i need your help with this task"
```

### Few-Shot Examples

**Example 1**

* Informal input: `hey can you send me the report`
* Formal output: `Could you please send me the report?`

**Example 2**

* Informal input: `i need the files today so send them asap`
* Formal output: `I would appreciate it if you could send me the files today as soon as possible.`

### Implementation

When `--few-shot` is enabled and the selected mode is `rewrite-formal`, the two examples are appended to the system prompt before sending the request to Gemini.

When the flag is omitted, the assistant uses the normal system prompt without these examples. The other writing modes continue to use their own prompts.

### Comparison and Testing

**Test input:** `hi i need your help with this task`

| Approach         | Observed output                                           |
| ---------------- | --------------------------------------------------------- |
| Without few-shot | Hello, I would appreciate your assistance with this task. |
| With few-shot    | Could you please assist me with this task?                |

Both outputs are professional and preserve the user's intended meaning. The wording differs between the two runs, demonstrating that the model can produce different valid rewrites with and without examples. However, one comparison does not establish that few-shot prompting is always better.

### Key Learning

Few-shot prompting provides examples of the desired input-output pattern. It can guide the model's response style, while the `--few-shot` flag allows users to enable or disable the examples.
