---
sidebar_position: 1
---

# Zero-Shot & Few-Shot Prompting

You've learned how to write clear, structured prompts — but sometimes, even clear instructions lead to confusing results.

Imagine you ask the model:
```
Write a short message to apologize to a friend for missing their birthday dinner. 
Make it sound sincere, friendly, and positive so the friend forgives me.
```

Sounds clear, right?

Yet the model might write:
> Hey, sorry I couldn't make it to your dinner. Hope it went great!

which is polite but sounds too casual or even indifferent.

> I deeply regret missing your dinner and hope you can find it in your heart to forgive me.

which sounds overly formal and dramatic for a friend.

Both are technically correct, but neither matches the warm, friendly tone you wanted — something like:
> Can't believe I missed your big night, Mia! I'm so sorry — I'll make it up to you this weekend. Hope you had the best time.

The model did what you asked — just not *how* you meant it.  
It didn't know your style, because you never showed it what "good" looks like.

Sometimes the task is simple enough that you don't need any examples. That's called **zero-shot prompting**.  
But other times, showing one or two examples makes all the difference and that's where **few-shot prompting** comes in.

---

## 1. What Is Zero-Shot Prompting

**Zero-shot prompting** means giving the model a clear instruction **without any examples or demonstrations**.

The model relies entirely on what it already knows from training to produce the result — like asking:
```
Translate the following English sentence into French: "The weather is nice today."
```

The model doesn't need you to show examples of translations — it's seen millions of them during training.

### When Zero-Shot Works Well

Zero-shot prompting is effective when:
- The task is **common and well-defined** (like translation, summarization, factual Q&A)
- The **desired output format** is obvious from the instruction
- You just need a **quick first attempt** to see how the model interprets your goal

It's perfect for testing ideas or building a baseline before refining your prompt further.

### When It Starts to Break Down

Zero-shot prompting struggles when:
- The task is **ambiguous** or **has multiple valid answers**
- The model must follow **specific tone, structure, or style rules** that aren't spelled out
- The output needs to match **your custom definition or criteria**

In these cases, the model can only guess your intent — and its guess might be wrong.

:::tip Zero-shot is your starting point
It teaches you how far clarity alone can take you. When instructions alone can't capture nuance, tone, or structure — that's your signal to use examples.
:::

---

## 2. What Is Few-Shot Prompting

**Few-shot prompting** means showing the model **a few examples of how a task should be done** before asking it to handle a new case — This helps it learn your tone, format, or reasoning pattern from those examples.

Let's say you want the model to turn customer feedback into a short, friendly summary.

**Without examples:**
```
Summarize this review in a friendly tone.
"The new update fixed all the bugs, runs perfectly now."
```
You might get inconsistent results — some formal, some casual.

**With examples:**
```
Review: "The app is easy to use but drains the battery fast."
Summary: "Great usability, but needs battery optimization."

Review: "Loved the design, but wish it had dark mode."
Summary: "Stylish and smooth — dark mode would make it perfect!"

Now summarize this one:
Review: "The new update fixed all the bugs, runs perfectly now."
```

The model learns the rhythm and tone from your examples and produces something like:
> Smooth, stable, and finally bug-free — great job!

It's consistent, friendly, and aligned with your examples — no guessing required.

### When to Use Few-Shot Prompting

Few-shot prompting is especially helpful when you want the model to:
- Follow a **specific tone, style, or voice**
- Produce outputs with a **consistent format or structure**
- Learn a **custom rule, scoring system, or labeling style**
- Handle **specialized or unfamiliar tasks** by imitation
- Improve **accuracy and reliability** through clearer context
- Generate **more predictable or repeatable results** across prompts

:::tip Prefer quality over quantity
Usually, **two to five examples** are enough. More examples can help with consistency, but too many may crowd the context and confuse the model.

The key is **clear, diverse, and consistent demonstrations**.
:::

---

## 3. Try It Yourself

Let's practice converting a zero-shot prompt into a few-shot prompt.

**Task:** Decide whether each message is formal or informal, and rewrite the informal ones to sound formal.

1. "Hey, can u send me that file real quick?"
2. "Could you please forward me the file when you have a moment?"
3. "Send me the file now!"

Start with a **zero-shot** prompt, then improve it into a **few-shot** version by adding **two labeled examples**.

---

<details>
<summary><strong>Example Answers</strong></summary>

<div>

**Zero-Shot Prompt:**
```
Classify each message as formal or informal. If informal, rewrite it to sound formal.

1. "Hey, can u send me that file real quick?"
2. "Could you please forward me the file when you have a moment?"
3. "Send me the file now!"
```

**Few-Shot Prompt:**
```
Classify each message as formal or informal. If informal, rewrite it to sound formal.

Example 1:
Message: "What's up? Can you send me that report?"
Classification: Informal
Formal Rewrite: "Hello, could you please send me the report?"

Example 2:
Message: "Please find the attached document."
Classification: Formal

Now classify and rewrite:
1. "Hey, can u send me that file real quick?"
2. "Could you please forward me the file when you have a moment?"
3. "Send me the file now!"
```

Notice how the examples show the model:
- **The exact format** to follow (Message, Classification, Formal Rewrite)
- **What counts as formal vs informal**
- **The style and tone** for rewrites

</div>
</details>

---

## What's Next

You've now learned how to **teach a model by example**.

But when your task needs **step-by-step thinking**, **traceable logic**, or **verifiable answers**, it's time to level up to **Chain-of-Thought (CoT)** — the next technique for improving reasoning and accuracy.