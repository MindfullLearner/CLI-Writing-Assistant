# Prompting Comparison — CLI Writing Assistant

## 1. Objective

The purpose of this comparison is to observe how standard prompting and few-shot prompting affect the output of the `rewrite-formal` mode in the CLI Writing Assistant.

Few-shot prompting provides examples of informal text and their corresponding formal rewrites. These examples help communicate the desired writing style to the model.

## 2. Test Setup

* **Model:** Gemini (`gemini-3.8-flash`)
* **Mode:** `rewrite-formal`
* **Test input:** `hi i need your help with this task`
* **Standard prompting:** Uses the regular system prompt without examples.
* **Few-shot prompting:** Uses the same system prompt with two informal-to-formal examples.

### Commands Used

Standard prompting:

```powershell
python assistant.py rewrite-formal "hi i need your help with this task"
```

Few-shot prompting:

```powershell
python assistant.py rewrite-formal --few-shot "hi i need your help with this task"
```

## 3. Observed Results

| Approach           | Observed output                                           |
| ------------------ | --------------------------------------------------------- |
| Standard prompting | Hello, I would appreciate your assistance with this task. |
| Few-shot prompting | Could you please assist me with this task?                |

Both outputs are professional, grammatically clear, and preserve the general intent of the original request.

The standard-prompt output uses a more elaborate, polite sentence. The few-shot output is shorter and directly asks for assistance.

## 4. Analysis

### Standard Prompting

The standard system prompt provides instructions about tone, grammar, clarity, and preservation of meaning. The model generates a formal rewrite based on these instructions.

**Observation:** The output is polite and professional without requiring additional examples.

### Few-Shot Prompting

The `--few-shot` flag adds two examples of informal text paired with formal rewrites to the system prompt.

**Observation:** In this test, the model produced a concise, polite request that followed the general style demonstrated by the examples.

### Key Difference

Standard prompting relies primarily on written instructions, while few-shot prompting combines instructions with example input-output pairs.

## 5. Conclusion

Both approaches successfully produced a suitable formal rewrite for the test input. The outputs differed in wording and length, but both preserved the user's general intent.

This single comparison does not establish that few-shot prompting is always better than standard prompting. More tests with different inputs would be needed to evaluate consistency, tone, and output quality.

## 6. Lessons Learned

* Clear system instructions can guide the model's tone and behavior.
* Few-shot examples provide additional guidance about the desired input-output pattern.
* Different prompting strategies can produce different valid outputs for the same input.
* Evaluating prompt quality requires multiple examples and consistent criteria, not just one successful response.
