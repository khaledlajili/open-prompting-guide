---
sidebar_position: 1
---

# Introduction to Prompt Engineering

You’ve probably chatted with an AI assistant — maybe asked it to write an email, explain a topic, or fix a bit of
code.  
Sometimes it gives exactly what you wanted, and sometimes it completely misses the point.

The difference isn’t magic — it’s **how you ask**.

This guide will show you how to turn your words into *clear instructions* that AI systems can actually understand —
helping you get more accurate, creative, and useful results.

Every AI assistant you’ve used — like ChatGPT or Claude — is powered by a **Large Language Model (LLM)**, a system that
generates text based on your instructions.

---

## 1. What Is a Prompt

A **prompt** is the text instruction you give to a language model to get a response.  
It can be a question, a task description, a block of structured text, or even an example to follow.

**Simple examples:**
```
- “Translate this sentence into Spanish.”
- “Write a friendly message to reschedule a meeting.”
- “List three fun facts about dolphins.”
```
Each one tells the model:

1. **What you want it to do** (e.g., translate, write, list)
2. **What information or context to use** (e.g., "this sentence", "reschedule a meeting", "dolphins")
3. **How the response should be framed** (e.g., in Spanish, friendly tone, as a list)

---

## 2. What Is Prompt Engineering

**Prompt engineering** means **designing and refining prompts** so that an LLM reliably delivers accurate,
well-organized, and useful responses.

It’s a mix of:

- **Communication skills** — writing clear, specific instructions the model can understand
- **System thinking** — structuring tasks, examples, and context in a logical way
- **Experimentation** — iterating, testing, and improving results

**Real-world examples:**

- Marketers create prompts that generate consistent brand voice.
- Developers write structured prompts to produce code safely.
- Students use reasoning prompts to explain complex concepts.

---

## 3. Why Prompting Matters: How Language Models Really Work

Language models can’t read your mind — they don’t “understand” your goals or intentions.  
Instead, they:

1. Predict one word at a time based on patterns in the input
2. Rely completely on the prompt and context you give them

That’s why **prompt engineering** is important:  
It helps you turn your intention into the kind of input a model can actually work with.

:::info Think of the model like a smart autocomplete
It doesn’t know what you *want* — only what’s *likely to come next* based on what you've typed.
:::
---

## 4. Prompt Elements

A clear prompt often contains a few simple parts.

| Element             | What It Means                              | Example                                         |
|---------------------|--------------------------------------------|-------------------------------------------------|
| **Instruction**     | What you want the model to do.             | “Summarize this article.”                       |
| **Input / Context** | The information you want the model to use. | “The article below explains our company goals.” |
| **Output Format**   | How you want the answer to be structured.  | “Respond in 3 bullet points.”                   |
| **Constraints**     | Extra rules like tone, style, or length.   | “Use formal tone. Max 100 words.”               |
| **Role / Persona**  | Who the model should pretend to be.        | “You are a professional copywriter.”            |

:::info Use what you need
You don’t need all of them every time, but knowing them helps you build better prompts.
:::
---

## 5. Tips for Crafting Clear and Effective Prompts

Good prompts are **specific**, **context-aware**, **constrained**, and **structured**.

| # | Tip & Explanation                                                      | Example                                                                                       |
|---|------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| 1 | **Start simple:** Describe what you actually want the model to do — one clear action.                            | “Write a report on renewable energy.”                                                                                                                          |
| 2 | **Be specific:** Be explicit about the topic, scope, and focus.                                                  | “Write a report *comparing solar and wind energy*.”                                                                                                            |
| 3 | **Add context:** Give background, purpose, or audience.                                                          | “Write a report comparing solar and wind energy *for a high-school science project*.”                                                                          |
| 4 | **Define output format:** Specify how you want the answer delivered.                                             | “Write a *short* report comparing solar and wind energy *in three paragraphs: introduction, comparison, and conclusion*.”                                      |
| 5 | **Set constraints:** Limit or guide the response (e.g., length, tone, focus, style) so it stays on target.       | “Write a *200-word formal* report comparing solar and wind energy, *focusing on advantages and disadvantages only*.”                                           |
| 6 | **Use positive, precise phrasing:** Tell the model what *to do*, not what *not to do*; avoid vague negatives.    | “Don’t make it too long.” → “Keep it under 200 words.”                                                                                                         |
| 7 | **Assign a role or perspective:** You can define a role to influence style and reasoning, but use it only when it adds value. | “*You are a science teacher*. Write a report comparing solar and wind energy.”                                                                                 |
| 8 | **Iterate and refine:** Review the output and adjust your prompt — add missing details or clarify unclear parts. | “You are a science teacher. Write a 200-word formal report comparing solar and wind energy for a high-school science project. Focus on advantages and disadvantages only. Structure your answer in three short paragraphs: introduction, comparison, and conclusion.” |

:::tip Think of a prompt as a mini-contract
“Here’s what you should do, what you know, the limits you must respect, and how to deliver it.”
:::
## 6. Try It Yourself

Let’s practice rewriting a vague prompt into strong, specific ones.

Take this vague prompt:
```
Write about healthy food.
```
Your goal is to **turn it into two clear prompts** — one for a *creative writing task* and one for a *factual information task*.

When you rewrite, remember to:
- Add **context** (like purpose, or audience).
- Add **constraints** (like length, tone, or focus).
- Specify the **output format** (paragraphs, list, table, etc.).
- Keep each prompt focused on *one purpose only*.

---

<details>
<summary>**Example Answers**</summary>

<div>

**Creative version**
```
Write a short, 150-word persuasive blog post encouraging teenagers to eat healthier meals. Use an inspiring and friendly tone.
```
- **context:** persuade, teenagers
- **constraints:** 150 words, inspiring and friendly tone
- **output format:** blog post

**Factual version**
```
For a high-school health class, write a concise, 120-word explanation listing 5 scientifically proven health benefits of a balanced diet. Use clear, neutral language and format your answer as bullet points.
```
- **context:** high-school health class
- **constraints:** 120 words, 5 benefits, neutral tone
- **output format:** bullet points

Together, they show how changing *context* and *constraints* completely changes the model’s output — even when the topic is the same.


</div>
</details>


---

## What’s Next

You now know **how to talk clearly to a language model** — the foundation of everything that follows.

But sometimes, even a perfectly worded prompt fails because the model hasn’t seen enough examples of what you mean.  
That’s where **Zero-Shot and Few-Shot prompting** come in — the next step in teaching models through examples.

