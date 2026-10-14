---
sidebar_position: 4
---

# Self-Consistency

Chain-of-Thought (CoT) prompting encourages language models to show their work step-by-step. But what happens if the model makes a minor arithmetic or logical misstep early on, the entire final answer falls apart.

Instead of relying on a single chain of thought, what if you generated multiple independent reasoning paths and took the majority vote?

This is the core concept behind **Self-Consistency**.

---

## 1. What Is Self-Consistency?

**Self-Consistency** is a prompting technique that generates multiple reasoning paths for the same question, then selects the answer that appears most often.

It is often combined with Chain-of-Thought prompting: the model tries different ways to solve a problem, and their final answers are compared.

---

## 2. How Self-Consistency Works

### Step 1: Prompt with Chain-of-Thought

Give the model a problem using Zero-Shot CoT ("Let's think step by step") or Few-Shot CoT examples showing step-by-step solutions.

### Step 2: Generate Multiple Reasoning Paths

Query the model multiple times (e.g., 3 to 10 runs) with a non-zero temperature parameter. This introduces slight variability, allowing the model to explore different ways to break down the problem.

### Step 3: Vote on the Final Answer

Aggregate the final answers from all generated paths. The answer that appears most frequently is chosen as the true output.

**Example prompt:**
```text
When I was 6 my sister was half my age. Now I’m 70, how old is my sister?
```
A single greedy run might over-simplify the math and output 35 (assuming she is always half your age).

With Self-Consistency we sample several paths. Typical outputs look like:
> Path 1: When I was 6 she was 3. Now I am 70, so she is 70 − 3 = 67.

> Path 2: Sister was 3 when I was 6. Age difference is 3 years. 70 − 3 = 67.

> Path 3: Half of 70 is 35, so she is 35 now. incorrect path
---

## 3. When to Use Self-Consistency

It can be useful for tasks where a small reasoning mistake changes the answer, such as:

- **Complex Arithmetic & Word Problems:** Math tasks where intermediate calculation mistakes are common.
- **Logic & Commonsense Reasoning:** Problems with multiple valid ways to deduce the correct answer.
- **High-Stakes Classification:** Scenarios where accuracy is far more important than token cost or latency.

It is less useful for simple tasks with an obvious answer, and generating multiple attempts takes more time and tokens. If every attempt makes the same mistake, self-consistency will not fix it.

---

## 4. Try It Yourself

Ask a model to solve this problem in five independent attempts, then compare the final answers:

```text
Solve this probability problem:
A fair coin is tossed repeatedly until one of these two patterns of five consecutive tosses appears:
- Pattern A: HHTHH
- Pattern B: HTHTT
What is the exact probability that Pattern A appears before Pattern B?
Solve the problem from first principles. Account for overlapping sequences and express your answer as a simplified fraction.
Provide your mathematical derivation and final answer.
```

<details>
<summary><strong>Example Answer</strong></summary>

| Attempt | Final probability |
|---|---------|
| 1 | (8/17)  |
| 2 | (8/17)  |
| 3 | (8/13)  |
| 4 | (8/17)  |
| 5 | (8/17)  |

**the winning answer : 8/17** (appears 4 out of 5 times)

</details>

---

## What's Next

You've now learned how to improve reliability by generating multiple reasoning paths and comparing their answers.

But sometimes, the model needs relevant knowledge before it can reason effectively about a problem.

That's where **Generated Knowledge Prompting** comes in — a technique that asks the model to generate relevant information before using it to answer a question.