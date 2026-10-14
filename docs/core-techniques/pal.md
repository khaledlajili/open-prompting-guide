---
sidebar_position: 13
---

# Program-Aided Language Models (PAL)

You’ve learned how to guide models using step-by-step reasoning, external tools, and automated pipelines.

However, even with Chain-of-Thought (CoT) prompting, large language models are fundamentally text predictors — not calculators. When faced with complex arithmetic, multi-step date calculations, or precise logic, LLMs frequently make simple math errors or hallucinate numbers because they generate answers token-by-token rather than executing actual math.

What if the model could translate the question into a small Python program and let a computer execute that program to calculate the answer?

This is the idea behind **Program-Aided Language Models (PAL)**.

---

## 1. What Is Program-Aided Language Models (PAL)?

**Program-Aided Language Models (PAL)** is a technique that uses LLMs to read natural language problems and generate computer programs (such as Python code) as intermediate reasoning steps.

Instead of using free-form text to arrive at a solution (like traditional CoT), PAL offloads the actual calculation and execution step to an external programmatic runtime (a Python interpreter).

---

## 2. How Program-Aided Language Models Works

The process is straightforward:

1. The model receives a natural language question (often with a few examples).
2. It generates a program that solves the question.
3. The program is executed in an interpreter.
4. The result of the execution is returned as the answer.

**Example question:**
```text
Today is 27 February 2023. I was born exactly 25 years ago. What is the date I was born in MM/DD/YYYY?
```

**Model-generated program (simplified):**
```python
from datetime import datetime
from dateutil.relativedelta import relativedelta

today = datetime(2023, 2, 27)
born = today - relativedelta(years=25)
print(born.strftime('%m/%d/%Y'))
```

**Execution result:**

> 02/27/1998


By letting the interpreter handle the date arithmetic, PAL avoids common language-model mistakes in calculation.

---

## 6. Advantages and Limitations of PAL

### Why Use PAL?

- **More reliable computation:** A programming runtime handles supported calculations directly instead of requiring the model to perform every operation through generated text.
- **Clear separation of responsibilities:** The LLM interprets the problem and generates the program; the runtime executes it.
- **Flexible problem solving:** The approach can support mathematical, symbolic, date-related, and algorithmic tasks that can be represented in code.
- **Inspectable intermediate representation:** The generated program can be examined to understand which operations the application will execute.
- **Integration with existing tools:** Programs can use suitable libraries and computational systems when these are available in the execution environment.

### An Important Security Consideration

Generated code must be treated as untrusted input.

A simple example can illustrate code execution using `exec()`, but **directly executing unrestricted model-generated code in a production application is unsafe**.

A malicious or incorrectly generated program could access files, consume excessive resources, or perform unintended operations.

A production system should use an appropriately restricted execution environment, validate allowed operations, impose resource limits, and prevent access to sensitive data and unnecessary system capabilities.

The exact safeguards depend on the application and runtime being used.

---

## 7. Try It Yourself

**Task:** Imagine you are building a PAL snippet to solve a financial calculation problem.

```text
An employee starts with a base salary of $50,000. They receive a 5% raise each year for 3 years. What is their salary at the end of Year 3?
```

Write a Python code snippet using basic variables or a loop that an LLM would generate for a PAL pipeline to solve this accurately.

<details>
<summary><strong>Example Answer</strong></summary>

**Generated PAL Code Snippet:**

```python
# Base salary calculation with compounding annual raises
salary = 50000
raise_rate = 0.05
years = 3

for year in range(years):
    salary = salary * (1 + raise_rate)

# Format the final answer
print(f"${salary:.2f}")
```

**Runtime Output:**

> 57881.25

</details>

---
## What's Next

You've now learned how **Program-Aided Language Models (PAL)** combine natural-language understanding with executable programs to solve computational problems.

The key is to **let the model interpret the problem and generate code while an execution environment handles the computation**.

But some tasks require more than executing a single program. They involve gathering information, observing results, and deciding what action to take next based on what happens.

That's where **ReAct (Reasoning and Acting)** comes in — an approach that interleaves reasoning, actions, and observations to help models solve tasks through interaction with external tools and environments.