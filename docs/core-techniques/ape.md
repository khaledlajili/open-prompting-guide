---
sidebar_position: 10
---

# Automatic Prompt Engineer (APE)

You’ve learned how to design prompts manually — from writing clear instructions and few-shot examples to structuring multi-step reasoning, RAG pipelines, and tool execution.

However, manually tweaking prompt phrasing, searching for optimal words, and testing subtle variations by hand is time-consuming and often relies on trial-and-error.

What if language models could write and optimize their own prompts automatically?

This is the idea behind **Automatic Prompt Engineer (APE)**.

---

## 1. What Is APE?

**Automatic Prompt Engineer (APE)** is a framework that automates instruction generation and selection. It frames prompt engineering as a natural language synthesis and black-box optimization problem, using language models to generate, evaluate, and search for the best-performing instructions for a given task.

Instead of relying entirely on human intuition, APE uses a language model to propose candidate instructions and evaluates those candidates using a target model.

---

## 2. How APE Works

The APE optimization process follows a two-stage loop:

### Stage 1: Candidate Instruction Generation

An inference model (LLM) is provided with input-output demonstrations of a task (e.g., pairs of math questions and their answers) and prompted to synthesize a high-level instruction that describes the task.

### Stage 2: Evaluation and Selection

1. **Execution:** The candidate instructions are appended to test inputs and executed using a target language model.
2. **Scoring:** The outputs are scored using an evaluation metric (e.g., execution accuracy or log-likelihood).
3. **Filtering & Refinement:** APE filters out weak instructions and can further propose subtle variations on top-scoring candidates to find the most effective instruction.

One notable result from the paper is that APE discovered a zero-shot Chain-of-Thought prompt that outperformed the well-known human-written phrase “Let’s think step by step.”

The automatically found prompt was:

```text
Let’s work this out in a step by step way to be sure we have the right answer.
```
---

## 6. Advantages and Limitations of APE

### Why Use APE?

- **Less manual trial and error:** APE can generate and evaluate many candidate instructions without requiring a person to write each version.
- **Measurable selection:** Candidates can be compared using task-specific evaluation metrics.
- **Potential performance improvements:** Automatically generated instructions can outperform manually written alternatives on particular tasks.
- **Reusable optimization process:** The same general approach can be applied to different tasks by changing the examples, target model, and evaluation criteria.

### What to Keep in Mind

APE does not guarantee that the selected prompt will be correct or effective in every situation.

- **Evaluation quality matters.** If the test examples or evaluation metric do not represent the real task, the selected instruction may optimize the wrong behavior.
- **Optimization can be expensive.** Generating and testing many candidates requires additional model calls, time, and computational resources.
- **Overfitting is possible.** A candidate might perform well on the examples used during selection but poorly on new inputs. Keeping a separate validation set helps identify this problem.
- **Results are model-dependent.** An instruction that works well with one model may not perform equally well with another.
- **Human review can still be useful.** Evaluation scores alone may not capture every important requirement, such as clarity, safety, consistency, or the correct handling of ambiguous inputs.

APE is therefore best understood as a way to improve prompt discovery and selection, not as a replacement for evaluation and human judgment.

---

## 8. Try It Yourself

**Task:** Simulate the APE instruction-generation stage manually by acting as the inference model.

**Input-Output Demonstrations:**

| Review | Expected Output |
|---|-----------------|
| The package was delivered late and damaged. Score: 1/5 | NEGATIVE        |
| Setup was straightforward and support was very helpful. Score: 5/5 | POSITIVE        |
| he item works as expected, nothing special. Score: 3/5 | NEUTRAL         |

Design a meta-prompt that asks an LLM to generate 3 candidate instructions that explain how to map these inputs to outputs.

<details>
<summary><strong>Example Answer</strong></summary>

**Meta-Prompt for Candidate Generation:**

```
You are an expert prompt optimization engine. Below are input-output demonstrations of a task.

Demonstrations:
- Input: "The package was delivered late and damaged. Score: 1/5" -> Output: Negative
- Input: "Setup was straightforward and support was very helpful. Score: 5/5" -> Output: Positive
- Input: "The item works as expected, nothing special. Score: 3/5" -> Output: Neutral

Task: Generate 3 distinct, concise instruction candidates that could be placed at the top of a prompt to guide a language model to perform this task accurately.

Instructions:
```

**Model's Generated Candidate Instructions:**

> Candidate A: "Analyze the customer review text and numerical score, then classify the sentiment as Positive, Neutral, or Negative."<br />
> Candidate B: "Assign a sentiment label (Positive/Neutral/Negative) based on the customer's satisfaction level indicated in the review."<br />
> Candidate C: "Determine the overall emotion of the feedback, using the 1-5 rating as supporting context."

(An APE framework would then test these 3 candidates against a validation set to select the winner!)

</details>

---
## What's Next

You've now learned how **Automatic Prompt Engineer (APE)** can generate and evaluate candidate instructions to discover which prompts work best for a particular task.

The key is to **treat prompt design as an optimization process rather than relying entirely on manual trial and error**.

But choosing better instructions doesn't necessarily solve every reasoning problem. Sometimes, the model struggles with specific questions, and human-written examples could help — if we knew which questions were worth annotating.

That's where **Active-Prompt** comes in — a technique that uses model uncertainty to identify the most informative questions for human annotation.