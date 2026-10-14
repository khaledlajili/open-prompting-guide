---
sidebar_position: 6
---

# Prompt Chaining

You’ve learned several ways to improve a single prompt: clearer instructions, examples, step-by-step reasoning, multiple attempts, and generated knowledge.

But what happens when a task involves several different operations, and asking the model to perform all of them at once makes the result harder to control?

Imagine you want an AI assistant to answer a question about a long document. The assistant must first find the relevant information, then understand it, and finally formulate an accurate answer.

Instead of asking the model to perform all these operations in a single prompt, you can separate them into smaller steps.

This is the idea behind **Prompt Chaining**.

---

## 1. What Is Prompt Chaining?

**Prompt Chaining** is a technique that breaks a complex task into smaller subtasks, where the output of one prompt becomes the input of the next prompt.

Think of it like an assembly line:
```
[ Raw Input ] ──► [ Prompt 1: Extract ] ──► [ Output 1 ] ──► [ Prompt 2: Transform ] ──► [ Final Output ]
```

Prompt chaining allows you to control each stage separately, making complex tasks easier to manage, inspect, and improve.

:::info The Modular Advantage
By isolating each subtask into its own prompt, you eliminate the cognitive overload that happens when a model tries to follow dozens of rules simultaneously.
:::

---

## 2. Why Use Prompt Chaining?

Splitting a complex workflow into multiple steps offers several major advantages over single-prompt approaches:

| Advantage | Why It Matters |
|---|---|
| Higher Accuracy & Reliability | "The model focuses on one simple objective at a time, drastically reducing errors and hallucinations."| 
| Greater Transparency & Debugging | "If the final answer is wrong, you can inspect each intermediate output to see exactly where the pipeline failed."| 
| Increased Controllability | "You can clean, reformat, or validate the output of Step 1 before feeding it into Step 2."| 
| Reusability | "Individual prompts (e.g., a ""Quote Extractor"" or ""Tone Refiner"") can be reused across different workflows."| 

---

## 3. How Prompt Chaining Works

Let's explore a practical example.

Imagine you are building an AI assistant that answers questions about documents. A user provides a document and asks a question about its content.

Instead of asking the model to read the document and immediately generate an answer, you can create a chain of prompts that handles the task in stages.

### Step 1: Extract Relevant Information

The first prompt identifies the passages that are relevant to the user's question.

**Prompt 1:**

```text
You are an assistant that extracts relevant information from documents.

Your task is to identify the passages that contain information
needed to answer the given question.

Question:
{{question}}

Document:
####
{{document}}
####

Instructions:
- Extract the most relevant passages from the document.
- Preserve the original wording of the selected passages.
- Do not answer the question yet.
- Do not introduce information that is not present in the document.
- If no relevant information is found, respond with:
  "No relevant passages found."

Return only the relevant passages.
```

Suppose the document contains the following information:

> Prompt chaining divides a complex task into smaller sequential subtasks. The output of one prompt becomes the input to the next prompt. This approach can improve controllability and make it easier to identify errors in individual stages.

The user asks:

**"What is prompt chaining, and what is one of its benefits?"**

The model's output could be:

> Prompt chaining divides a complex task into smaller<br />
> sequential subtasks.<br />
> The output of one prompt becomes the input to the next prompt.<br />
> This approach can improve controllability and make it easier<br />
> to identify errors in individual stages.

### Step 2: Generate the Answer

Now, the second prompt uses the extracted passages to formulate a clear and accurate answer.

**Prompt 2:**

```text
You are a helpful assistant answering questions about documents.

Use the relevant passages extracted from the document to answer
the original question.

Question:
{{question}}

Relevant passages:
####
{{relevant_passages}}
####

Instructions:
- Answer the question clearly and directly.
- Base your answer on the relevant passages.
- Do not invent information that the passages do not support.
- If the passages do not contain enough information to answer
  the question, explain that the information is insufficient.

Write the final answer in a concise paragraph.
```

**Model response:**

> Prompt chaining breaks a complex task into smaller steps, passing each step's output to the next. It improves control over the process and makes errors easier to identify.

## 3. Common Use Cases for Prompt Chaining

Prompt chaining is most useful when a task contains several distinct operations that benefit from being handled separately.

### Tasks Where It Can Help

| Situation | How Prompt Chaining Helps |
|---|---|
| Document question answering | Extracts relevant passages before generating an answer. |
| Research and analysis | Organizes research, analyzes findings, and then prepares a report. |
| Content creation | Develops an outline, writes a draft, and then improves the writing. |
| Data processing | Classifies information, extracts specific fields, and transforms the results into a structured format. |
| AI-powered applications | Separates operations into manageable stages that developers can inspect and improve. |

:::tip Keep intermediate outputs structured
When passing data between chain steps, use clear delimiters like XML tags (<quotes></quotes>), Markdown blocks, or JSON. This helps subsequent prompts easily identify the data they need to process.
:::

### When It May Be Less Effective

Prompt chaining may be less useful when:

- The task is simple enough to complete reliably with a single prompt.
- The subtasks do not need to be separated to achieve the desired result.
- The additional steps introduce unnecessary complexity, processing time, or cost.
- An early step generates incorrect information that later steps rely on.

:::warning More steps do not automatically mean better results
Errors can propagate through a prompt chain. If the first prompt extracts incorrect information, the second prompt may produce a convincing answer based on that mistake.
:::

---

## 4. Try It Yourself

**Task:** Design a 2-step prompt chain to handle a negative customer review.

- **Step 1:** Extract the core issues and customer emotion from the raw review.
- **Step 2:** Use the extracted details from Step 1 to generate an empathetic response email offering a solution.

**Raw Review:**
```text
I ordered my couch three weeks ago and it was supposed to arrive in five days. When it finally arrived today, the wood on the left armrest was cracked! Customer support kept me on hold for 40 minutes when I called.
```
<details>
<summary><strong>Example Answer</strong></summary>

**Step 1 — Step 1: Extraction Prompt**

```text
Extract the key details from the customer review below.

Review:
{{ raw_review }}

Format your output as:
- Primary Emotion: [Emotion]
- Specific Complaints: [Bulleted list of issues]
```

**Model output 1:**

> - Primary Emotion: Frustrated and disappointed<br />
> - Specific Complaints:<br />
>     * Severe shipping delay (3 weeks instead of 5 days)<br />
>     * Damaged product (cracked wooden armrest)<br />
>     * Poor customer service experience (40-minute hold time)

---

**Step 2 — Response Generation Prompt**

```text
You are a Customer Experience Manager. Write an empathetic apology email to a customer based on the following diagnostic details:

{{ extracted_details }}

Instructions:
- Acknowledge each specific complaint directly.
- Maintain a warm, sincere, and professional tone.
- Offer a replacement armrest/couch and a 20% partial refund for the inconvenience.
```

**Model Output 2:**

> Dear Customer,<br />
> I am truly sorry to hear about your experience with your recent couch order. Waiting three weeks for a delivery that was promised in five days is completely unacceptable, and I deeply apologize for the frustration this caused.<br />
> Furthermore, receiving a damaged item with a cracked armrest after that delay — and then having to wait on hold for 40 minutes — is far below the standard of service we aim to provide.<br />
> To make this right, I have personally requested an immediate priority replacement for your couch at no additional cost. Additionally, I have processed a 20% refund back to your original payment method to compensate for the inconvenience and wait time.<br />
> Please let me know if this solution works for you, and I will personally track your replacement shipment.<br />
> Sincerely,<br />
> Customer Experience Team

</details>

---

## What's Next

## What's Next

You've now learned how to break complex tasks into smaller steps, using the output of one prompt as the input for the next.

But what if a problem requires exploring multiple possible approaches before deciding which one is most promising?

That's where **Tree of Thoughts** comes in — a technique that explores multiple reasoning paths, evaluates intermediate ideas, and helps the model navigate toward better solutions.